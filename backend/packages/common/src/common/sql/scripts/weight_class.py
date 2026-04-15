from collections.abc import Sequence

from loguru import logger
from sqlalchemy import ColumnElement, func, literal, select, update
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from common.models.weight_class import WeightClassStatus
from common.models.weight_class.weight_class import WeightClassification
from common.sql.tables import WeightClassificationTable, WheelReadingTable
from common.types import WeightClassId


def cdf(
    x: ColumnElement[float] | InstrumentedAttribute[float],
    mu: ColumnElement[float] | InstrumentedAttribute[float],
    std: ColumnElement[float] | InstrumentedAttribute[float],
) -> ColumnElement[float]:
    p = 0.5 * (1 + func.erf((x - mu) / (std * func.sqrt(2))))
    return 2 * func.least(p, 1 - p)


async def try_set_weight_class_status(
    session: AsyncSession,
    weight_class_ids: Sequence[WeightClassId],
    status: WeightClassStatus,
) -> list[WeightClassification]:

    statement = (
        update(WeightClassificationTable).where(WeightClassificationTable.id.in_(weight_class_ids)).values(status=status).returning(WeightClassificationTable)
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
    models = [t.m() for t in results]
    logger.success("Status set", result_ids=[m.id for m in models])
    return models
