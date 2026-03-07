from faust import StreamT
from loguru import logger

from common.kafka.faust import faust_app
from common.kafka.messages.weight_class import WeightClassificationCreated
from common.kafka.topics import WeightClassificationCreatedTopic


@faust_app.agent(
    WeightClassificationCreatedTopic,
    name="WeightClassification.SplitFrames",
)
async def split_frames(stream: StreamT[WeightClassificationCreated]) -> None:
    """Dowloads video from S3 and runs trought tire identification and Kalman filter, producing tire bbxs"""
    async for message in stream:
        logger.info(message.dumps())
