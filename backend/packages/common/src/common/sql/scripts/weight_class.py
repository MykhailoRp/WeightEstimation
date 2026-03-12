from collections.abc import Sequence

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.weight_class import WeightClassStatus
from common.sql.tables.weight_class import WeightClassificationTable
from common.sql.tables.wheel_reading import WheelReadingTable
from common.types import WeightClassId


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
                select(WheelReadingTable.weight_class_id.label("id"), func.bool_and(WheelReadingTable.masked_features.is_not(None)).label("check"))
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

    results = await session.scalars(statement)
    return list(results.all())
