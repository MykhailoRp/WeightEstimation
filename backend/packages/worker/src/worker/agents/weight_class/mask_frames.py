import asyncio

from faust import StreamT
from loguru import logger

from common.kafka.faust import faust_app
from common.kafka.messages.weight_class import WeightClassificationFrameCreated
from common.kafka.topics import WeightClassificationFrameCreatedTopic
from worker.singletons import client_maker, feature_extractor_maker, session_maker

MAX_FRAMES_BATCH = 5


@faust_app.agent(
    WeightClassificationFrameCreatedTopic,
    name="WeightClassification.MaskFrames",
)
async def mask_frames(stream: StreamT[WeightClassificationFrameCreated]) -> None:
    """Dowloads frame"""
    async for messages in stream.take(MAX_FRAMES_BATCH, within=3):
        with logger.contextualize(messages_sz=len(messages)):
            s3_client = client_maker()
            db_session = session_maker
            feature_extractor = feature_extractor_maker()

            logger.info("Extracting features...")
            await asyncio.to_thread(
                asyncio.run,
                feature_extractor.extract_features(
                    requests=messages,
                    db_session=db_session,
                    s3_client=s3_client,
                ),
            )
            logger.success("Features extracted")
