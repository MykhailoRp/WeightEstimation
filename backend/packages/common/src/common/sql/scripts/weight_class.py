from collections.abc import Sequence

from loguru import logger
from sqlalchemy import ColumnElement, and_, case, func, literal, select, update
from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from common.models.weight_class import WeightClassStatus
from common.models.weight_class.weight_class import WeightClassResult
from common.sql.tables.weight_class import WeightClassificationTable
from common.sql.tables.wheel_aggregation import WheelAggregationTable
from common.sql.tables.wheel_reading import WheelReadingTable
from common.types import WeightClassId


def cdf(
    x: ColumnElement[float] | InstrumentedAttribute[float],
    mu: ColumnElement[float] | InstrumentedAttribute[float],
    std: ColumnElement[float] | InstrumentedAttribute[float],
) -> ColumnElement[float]:
    p = 0.5 * (1 + func.erf((x - mu) / (std * func.sqrt(2))))
    return 2 * func.least(p, 1 - p)


async def try_set_weight_class_status(session: AsyncSession, weight_class_ids: Sequence[WeightClassId], status: WeightClassStatus) -> list[WeightClassId]:

    statement = (
        update(WeightClassificationTable)
        .where(WeightClassificationTable.id.in_(weight_class_ids))
        .values(status=status)
        .returning(WeightClassificationTable.id)
    )

    match status:
        case WeightClassStatus.PENDING:
            pass
        case WeightClassStatus.FRAMES_SPLIT:
            pass
        case WeightClassStatus.MASKS_EXTRACTED:
            wheel_features_extracted = (
                select(
                    WheelReadingTable.weight_class_id.label("id"),
                    func.bool_and(WheelReadingTable.masked_features.is_distinct_from(literal(None, JSONB))).label("check"),
                )
                .group_by(WheelReadingTable.weight_class_id)
                .where(WheelReadingTable.weight_class_id.in_(weight_class_ids))
                .cte("wheel_features_extracted")
            )
            statement = statement.where(
                WeightClassificationTable.id == wheel_features_extracted.c.id,
                wheel_features_extracted.c.check,
            )
        case WeightClassStatus.FEATURES_EXTRACTED:
            pass
        case WeightClassStatus.COMPLETED:
            pass

    logger.info("Setting status", status=status, request_ids=weight_class_ids)
    results = await session.scalars(statement)
    result_ids = list(results.all())
    logger.success("Status set", result_ids=result_ids)
    return result_ids


async def generate_aggregations(
    session: AsyncSession,
    weight_class_ids: list[WeightClassId],
    *,
    compression_lower: float = 0.4,
    compression_upper: float = 1.2,
) -> None:

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

    statement = insert(WheelAggregationTable).from_select(["weight_class_id", "id", "median", "std"], aggregations)

    await session.execute(statement)


async def predict_result(session: AsyncSession, vehicle_identifier: str, weight_class_id: WeightClassId) -> WeightClassResult | None:
    label = func.coalesce(WeightClassificationTable.result, WeightClassificationTable.assigned).label("label")

    distributions = (
        select(
            WheelAggregationTable.id,
            func.avg(WheelAggregationTable.median).filter(label == WeightClassResult.LOADED).label("loaded_mean"),
            func.stddev_pop(WheelAggregationTable.median).filter(label == WeightClassResult.LOADED).label("loaded_std"),
            func.avg(WheelAggregationTable.median).filter(label == WeightClassResult.EMPTY).label("empty_mean"),
            func.stddev_pop(WheelAggregationTable.median).filter(label == WeightClassResult.EMPTY).label("empty_std"),
        )
        .where(WeightClassificationTable.id != weight_class_id, WeightClassificationTable.vehicle_identifier == vehicle_identifier)
        .join(WeightClassificationTable, onclause=WeightClassificationTable.id == WheelAggregationTable.weight_class_id)
        .group_by(WheelAggregationTable.id)
        .cte("distributions")
    )

    loaded_score = cdf(WheelAggregationTable.median, distributions.c.loaded_mean, distributions.c.loaded_std).label("loaded_score")
    empty_score = cdf(WheelAggregationTable.median, distributions.c.empty_mean, distributions.c.empty_std).label("empty_score")

    confidance = func.greatest(loaded_score, empty_score) / (loaded_score + empty_score).label("confidance")
    wheel_prediction = case(
        (loaded_score > empty_score, WeightClassResult.LOADED),
        else_=WeightClassResult.EMPTY,
    ).label("prediction")

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
    )

    statement = (
        update(WeightClassificationTable)
        .values(result=prediction)
        .where(WeightClassificationTable.id == weight_class_id)
        .returning(WeightClassificationTable.result)
    )

    final_result = await session.scalar(statement)

    return final_result
