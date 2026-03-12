# from sqlalchemy import update
# from sqlalchemy.ext.asyncio import AsyncSession

# from common.models.weight_class import WeightClassStatus
# from common.sql.tables.weight_class import WeightClassificationTable
# from common.types import WeightClassId


# async def try_set_weight_class_status(session: AsyncSession, weight_class_id: WeightClassId, status: WeightClassStatus) -> bool:

#     statement = update(WeightClassificationTable).where(WeightClassificationTable.id == weight_class_id).values(status=status)

#     match status:
#         case WeightClassStatus.PENDING:
#             pass
#         case WeightClassStatus.FRAMES_SPLIT:
#             statement = statement.where()
#         case WeightClassStatus.MASKS_EXTRACTED:
#             statement = statement.where()
#         case WeightClassStatus.FEATURES_EXTRACTED:
#             statement = statement.where()
#         case WeightClassStatus.COMPLETED:
#             statement = statement.where()
