from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from api.dependencies import DBSession, S3Client, TokenData
from api.models.weight_class import WeightClassificationResponse
from api.models.weight_class.new import NewWeightClassification
from common.kafka.messages.weight_class import WeightClassificationCreated
from common.kafka.topics import WeightClassificationCreatedTopic
from common.models.user import UserRole
from common.sql.tables import WeightClassificationTable

router = APIRouter()


@router.post("/", status_code=200, operation_id="Create New Weight Classification")
async def create_weight_classification(
    request: Annotated[NewWeightClassification, Body()],
    session_maker: DBSession,
    token_data: TokenData,
    s3_client: S3Client,
) -> WeightClassificationResponse:

    if token_data.id != request.customer_id and not token_data.is_(UserRole.ADMIN):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cant upload on behalf of this user")

    result = request.create(
        video_key=s3_client.config.get_weight_class_video,
    )

    await s3_client.move_from_uploads(file_id=request.file_id, to=result.video_key)

    try:
        async with session_maker() as session:
            session.add(WeightClassificationTable.new(result))
            await session.commit()
    except:
        await s3_client.delete_object(result.video_key)
        raise
    else:
        await s3_client.delete_upload(request.file_id)

    await WeightClassificationCreatedTopic.send(
        key=WeightClassificationCreated.key(result.id),
        value=WeightClassificationCreated.new(result).model_dump_json(),
    )

    return WeightClassificationResponse.new(
        result,
        await s3_client.sign_url(result.video_key),
    )
