from typing import Annotated

from fastapi import APIRouter, Body, Path

from api.dependencies import DBSession, S3Client
from api.models.weight_class import NewWeightClassification
from common.models.weight_class import WeightClassification
from common.sql.tables import WeightClassificationTable
from common.types import UserId

router = APIRouter()


@router.post("/", status_code=200, operation_id="Create New Weight Classification")
async def create_weight_classification(
    user_id: Annotated[UserId, Path()],
    request: Annotated[NewWeightClassification, Body()],
    session_maker: DBSession,
    s3_client: S3Client,
) -> WeightClassification:

    result = request.create(
        user_id=user_id,
        video_url=s3_client.config.get_weight_class_video,
    )

    await s3_client.move_from_uploads(file_id=request.file_id, to=result.video_url)

    async with session_maker() as session:
        session.add(WeightClassificationTable.new(result))
        await session.commit()

    return result
