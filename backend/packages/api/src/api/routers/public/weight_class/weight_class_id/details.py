from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from api.dependencies import DBSession, S3Client, TokenData
from api.models.weight_class import WeightClassificationResponse
from common.models.user import UserRole
from common.sql.scripts.getters import get_weight_classification as get_weight_classification_script
from common.types import WeightClassId

router = APIRouter()


@router.get("/", status_code=200, operation_id="Get Weight Classification Details")
async def get_weight_classification(
    weight_class_id: Annotated[WeightClassId, Path()],
    session_maker: DBSession,
    token_data: TokenData,
    s3_client: S3Client,
) -> WeightClassificationResponse:

    async with session_maker() as session:
        classification = await get_weight_classification_script(
            session,
            id=weight_class_id,
            customer_id=None if token_data.is_(UserRole.ADMIN) else token_data.id,
        )

    if classification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Weight classification not found")

    return WeightClassificationResponse.new(
        classification,
        await s3_client.sign_url(classification.video_key),
    )
