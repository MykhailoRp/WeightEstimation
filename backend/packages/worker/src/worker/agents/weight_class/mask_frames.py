from faust import StreamT
from loguru import logger

from common.kafka.faust import faust_app
from common.kafka.messages.weight_class import WheelReadingCreated
from common.kafka.topics import WheelReadingCreatedTopic
from worker.singletons import client_maker, feature_extractor_maker, session_maker

MAX_FRAMES_BATCH = 15


@faust_app.agent(
    WheelReadingCreatedTopic,
    name="WeightClassification.MaskFrames",
)
async def mask_frames(stream: StreamT[bytes]) -> None:
    """Dowloads frame"""
    async for messages_bytes in stream.take(MAX_FRAMES_BATCH, within=3):
        messages = [WheelReadingCreated.model_validate_json(message_bytes) for message_bytes in messages_bytes]
        with logger.contextualize(messages_sz=len(messages)):
            s3_client = client_maker()
            db_session = session_maker
            feature_extractor = feature_extractor_maker()

            logger.info("Extracting features...")
            await feature_extractor.extract_features(
                requests=messages,
                db_session=db_session,
                s3_client=s3_client,
            )
            logger.success("Features extracted")
