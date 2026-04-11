from loguru import logger
from sqlalchemy import Enum, and_, case, delete, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from common.kafka.messages.weight_class import WeightClassificationCompleted, WeightClassificationMasked
from common.kafka.topics import WeightClassificationCompletedTopic
from common.models.weight_class.weight_class import WeightClassResult, WeightClassStatus
from common.models.weight_class.wheel_aggregation import WheelAggregation
from common.sql.scripts.weight_class import cdf
from common.sql.tables import WeightClassificationTable, WheelAggregationTable, WheelReadingTable
from common.types import UserId, WeightClassId


async def preclean_aggregations(
    session: AsyncSession,
    weight_class_ids: list[WeightClassId],
) -> None:
    await session.execute(delete(WheelAggregationTable).where(WheelAggregationTable.weight_class_id.in_(weight_class_ids)))


async def generate_aggregations(
    session: AsyncSession,
    weight_class_ids: list[WeightClassId],
    *,
    compression_lower: float = 0.4,
    compression_upper: float = 1.2,
) -> list[WheelAggregation]:

    q1 = func.percentile_cont(0.25).within_group(WheelReadingTable.compression.asc()).label("q1")
    q3 = func.percentile_cont(0.75).within_group(WheelReadingTable.compression.asc()).label("q3")
    iqr = (1.5 * (q3 - q1)).label("iqr")

    outlier_filter = (
        select(
            WheelReadingTable.weight_class_id,
            WheelReadingTable.id,
            (q1 - iqr).label("lower"),
            (q3 + iqr).label("upper"),
        )
        .group_by(
            WheelReadingTable.weight_class_id,
            WheelReadingTable.id,
        )
        .where(
            WheelReadingTable.weight_class_id.in_(weight_class_ids),
            WheelReadingTable.compression.between(compression_lower, compression_upper),
        )
        .cte("outlier_filter")
    )

    wheel_median = func.percentile_cont(0.5).within_group(WheelReadingTable.compression.asc()).label("median")
    wheel_std = func.stddev_pop(WheelReadingTable.compression).label("std")

    aggregations = (
        select(
            WheelReadingTable.weight_class_id,
            WheelReadingTable.id,
            wheel_median,
            wheel_std,
        )
        .where(
            WheelReadingTable.weight_class_id.in_(weight_class_ids),
            WheelReadingTable.compression.between(outlier_filter.c.lower, outlier_filter.c.upper),
        )
        .join(
            outlier_filter,
            onclause=and_(outlier_filter.c.weight_class_id == WheelReadingTable.weight_class_id, outlier_filter.c.id == WheelReadingTable.id),
        )
        .group_by(WheelReadingTable.weight_class_id, WheelReadingTable.id)
    )

    statement = insert(WheelAggregationTable).from_select(["weight_class_id", "id", "median", "std"], aggregations).returning(WheelAggregationTable)

    results = await session.scalars(statement)
    return [r.m() for r in results]


async def predict_result(
    session: AsyncSession,
    vehicle_identifier: str,
    weight_class_id: WeightClassId,
    customer_id: UserId,
    default_std: float = 0.05,
) -> WeightClassResult | None:
    label = func.coalesce(WeightClassificationTable.result, WeightClassificationTable.assigned).label("label")

    loaded_mean = func.avg(WheelAggregationTable.median).filter(label == WeightClassResult.LOADED)
    loaded_std = func.nullif(func.stddev_pop(WheelAggregationTable.median).filter(label == WeightClassResult.LOADED), 0)
    empty_mean = func.avg(WheelAggregationTable.median).filter(label == WeightClassResult.EMPTY)
    empty_std = func.nullif(func.stddev_pop(WheelAggregationTable.median).filter(label == WeightClassResult.EMPTY), 0)

    converted_loaded_mean = empty_mean * 0.918
    converted_empty_mean = loaded_mean * 1.088

    safe_loaded_mean = func.coalesce(loaded_mean, converted_loaded_mean).label("loaded_mean")
    safe_loaded_std = func.coalesce(loaded_std, empty_std, default_std).label("loaded_std")
    safe_empty_mean = func.coalesce(empty_mean, converted_empty_mean).label("empty_mean")
    safe_empty_std = func.coalesce(empty_std, loaded_std, default_std).label("empty_std")

    distributions = (
        select(
            WheelAggregationTable.id,
            safe_loaded_mean,
            safe_loaded_std,
            safe_empty_mean,
            safe_empty_std,
        )
        .where(
            WeightClassificationTable.id != weight_class_id,
            WeightClassificationTable.customer_id == customer_id,
            WeightClassificationTable.vehicle_identifier == vehicle_identifier,
        )
        .join(WeightClassificationTable, onclause=WeightClassificationTable.id == WheelAggregationTable.weight_class_id)
        .group_by(WheelAggregationTable.id)
        .cte("distributions")
    )

    loaded_score = cdf(WheelAggregationTable.median, distributions.c.loaded_mean, distributions.c.loaded_std).label("loaded_score")
    empty_score = cdf(WheelAggregationTable.median, distributions.c.empty_mean, distributions.c.empty_std).label("empty_score")

    confidance = func.greatest(loaded_score, empty_score) / (loaded_score + empty_score).label("confidance")
    wheel_prediction = (
        case(
            (loaded_score > empty_score, WeightClassResult.LOADED),
            else_=WeightClassResult.EMPTY,
        )
        .cast(Enum(WeightClassResult, name="weightclassresult"))
        .label("prediction")
    )

    prediction = (
        select(
            func.mode().within_group(wheel_prediction.asc()).label("prediction"),
        )
        .join(distributions, onclause=distributions.c.id == WheelAggregationTable.id)
        .where(
            # todo; move to config
            WheelAggregationTable.std < 0.12,
            confidance > 0.65,
            WheelAggregationTable.id.not_in([0]),  # ignore wheel under cabin
        )
        .scalar_subquery()
    )

    statement = (
        update(WeightClassificationTable)
        .values(result=prediction, status=WeightClassStatus.COMPLETED)
        .where(WeightClassificationTable.id == weight_class_id)
        .returning(WeightClassificationTable.result)
    )

    final_result = await session.scalar(statement)

    return final_result


async def extract_results(db_session: async_sessionmaker[AsyncSession], requests: list[WeightClassificationMasked]) -> None:
    async with db_session() as session:
        await preclean_aggregations(
            session=session,
            weight_class_ids=[r.id for r in requests],
        )

        await generate_aggregations(
            session=session,
            weight_class_ids=[r.id for r in requests],
        )

        results: dict[WeightClassId, WeightClassResult | None] = {}

        for r in requests:
            pred = await predict_result(
                session=session,
                weight_class_id=r.id,
                customer_id=r.customer_id,
                vehicle_identifier=r.vehicle_identifier,
            )
            results[r.id] = pred

        await session.commit()

    logger.success(
        "Assigned results",
        loaded=[r.id for r in requests if results.get(r.id) is WeightClassResult.LOADED],
        empty=[r.id for r in requests if results.get(r.id) is WeightClassResult.EMPTY],
        none=[r.id for r in requests if results.get(r.id) is None],
    )

    for r in requests:
        await WeightClassificationCompletedTopic.send(
            key=WeightClassificationCompleted.key(r.vehicle_identifier),
            value=WeightClassificationCompleted(
                id=r.id,
                vehicle_identifier=r.vehicle_identifier,
            ).model_dump_json(),
        )
