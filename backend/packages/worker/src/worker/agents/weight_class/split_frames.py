from faust import StreamT
from loguru import logger

from common.kafka.faust import faust_app
from common.kafka.messages.weight_class import WeightClassificationCreated
from common.kafka.topics import weight_classification_created


@faust_app.agent(
    weight_classification_created,
    name="WeightClassification.SplitFrames",
)
async def split_frames(stream: StreamT[WeightClassificationCreated]) -> None:
    """Dowloads uploaded video from S3 and runs trought tire identification and Kalman filter, producing tire bbxs"""
    async for message in stream:
        logger.info(message.dumps())
