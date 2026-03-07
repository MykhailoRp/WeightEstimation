from typing import Self

from common.kafka.messages import BaseMessage
from common.models.weight_class import WeightClassification
from common.types import WeightClassId


class WeightClassificationCreated(BaseMessage):
    id: WeightClassId
    video_url: str

    @classmethod
    def new(cls, model: WeightClassification) -> Self:
        return cls(
            id=model.id,
            video_url=model.video_url,
        )
