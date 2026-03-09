from typing import Self

from common.kafka.messages import BaseMessage
from common.models.weight_class import Frame, WeightClassification
from common.models.weight_class.frame import WheelBBX
from common.types import FrameId, S3Key, WeightClassId


class WeightClassificationCreated(BaseMessage):
    id: WeightClassId
    video_key: S3Key

    @classmethod
    def new(cls, model: WeightClassification, /) -> Self:
        return cls(
            id=model.id,
            video_key=model.video_key,
        )


class WeightClassificationFrameCreated(BaseMessage):
    id: FrameId
    weight_class_id: WeightClassId
    wheel_bbxs: list[WheelBBX]
    s3_key: S3Key

    @classmethod
    def new(cls, model: Frame, /) -> Self:
        return cls(
            id=model.id,
            weight_class_id=model.weight_class_id,
            wheel_bbxs=model.wheel_bbxs,
            s3_key=model.s3_key,
        )
