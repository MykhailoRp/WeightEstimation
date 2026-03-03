from common.kafka.messages import BaseMessage
from common.types import WeightClassId


class WeightClassificationCreated(BaseMessage):
    id: WeightClassId
    video_url: str
