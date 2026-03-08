from typing import Self

from common.kafka.messages import BaseMessage
from common.models.weight_class import WeightClassification
from common.types import S3Key, WeightClassId


class WeightClassificationCreated(BaseMessage):
    id: WeightClassId
    video_key: S3Key

    @classmethod
    def new(cls, model: WeightClassification) -> Self:
        return cls(
            id=model.id,
            video_key=model.video_key,
        )
