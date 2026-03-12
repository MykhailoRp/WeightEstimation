from typing import Self

from common.kafka.messages import BaseMessage
from common.models.weight_class import WeightClassification
from common.models.weight_class.wheel_reading import WheelFeatures, WheelReading
from common.types import FrameId, S3Key, WeightClassId, WheelId


class WeightClassificationCreated(BaseMessage):
    id: WeightClassId
    video_key: S3Key

    @staticmethod
    def key(id: WeightClassId) -> str:
        return id.__str__()

    @classmethod
    def new(cls, model: WeightClassification, /) -> Self:
        return cls(
            id=model.id,
            video_key=model.video_key,
        )


class WeightClassificationMasked(BaseMessage):
    id: WeightClassId

    @staticmethod
    def key(id: WeightClassId) -> str:
        return id.__str__()

    @classmethod
    def new(cls, id: WeightClassId, /) -> Self:
        return cls(
            id=id,
        )


class WheelReadingCreated(BaseMessage):
    weight_class_id: WeightClassId
    frame_id: FrameId
    id: WheelId
    raw_features: WheelFeatures
    s3_key: S3Key

    @staticmethod
    def key() -> None:
        return None

    @classmethod
    def new(cls, model: WheelReading, s3_key: S3Key) -> Self:
        return cls(
            weight_class_id=model.weight_class_id,
            frame_id=model.frame_id,
            id=model.id,
            raw_features=model.raw_features,
            s3_key=s3_key,
        )
