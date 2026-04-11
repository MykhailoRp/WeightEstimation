from typing import Annotated

from fastapi import APIRouter, Body

from api.dependencies import ApiUser, DBSession, S3Client
from api.models.weight_class import PublicNewWeightClassification, WeightClassificationResponse
from common.kafka.messages.weight_class import WeightClassificationCreated
from common.kafka.topics import WeightClassificationCreatedTopic
from common.sql.tables import WeightClassificationTable

router = APIRouter()


@router.post("/", status_code=200, operation_id="New New Weight Classification")
async def create_weight_classification(
    request: Annotated[PublicNewWeightClassification, Body()],
    session_maker: DBSession,
    token_data: ApiUser,
    s3_client: S3Client,
) -> WeightClassificationResponse:

    result = request.create(
        customer_id=token_data.customer_id,
        video_key=s3_client.config.get_weight_class_video,
    )

    await s3_client.move_from_uploads(uploader=token_data.customer_id, file_id=request.file_id, to=result.video_key)

    try:
        async with session_maker() as session:
            session.add(WeightClassificationTable.new(result))
            await session.commit()
    except:
        await s3_client.delete_object(result.video_key)
        raise
    else:
        await s3_client.delete_upload(request.file_id, uploader=token_data.customer_id)

    await WeightClassificationCreatedTopic.send(
        key=WeightClassificationCreated.key(result.id),
        value=WeightClassificationCreated.new(result).model_dump_json(),
    )

    return WeightClassificationResponse.new(
        result,
        await s3_client.sign_url(result.video_key),
    )
