from typing import TYPE_CHECKING, Self

from pydantic import BaseModel

from common.models.bounding_box import BoundingBox
from common.types import FrameId, S3Key, WeightClassId, WheelId

if TYPE_CHECKING:
    from common.models.weight_class.frame import Frame


class WheelFeatures(BaseModel):
    rim: BoundingBox
    tire: BoundingBox

    def get_compression(self) -> float:
        try:
            bottom_compression = self.rim.w / self.rim.h * ((self.tire.y + self.tire.h) - (self.rim.y + self.rim.h))
            left_perc = bottom_compression / (self.rim.x - self.tire.x)
            right_perc = bottom_compression / ((self.tire.x + self.tire.w) - (self.rim.x + self.rim.w))
            return (left_perc + right_perc) / 2
        except ZeroDivisionError:
            return 0.0


class WheelBBX(WheelFeatures):
    id: WheelId

    def as_features(self) -> WheelFeatures:
        return WheelFeatures(
            rim=self.rim,
            tire=self.tire,
        )


class WheelReadingData(BaseModel):
    rim_mask_key: S3Key | None = None
    tire_mask_key: S3Key | None = None
    model_name: str | None = None


class WheelReading(BaseModel):
    weight_class_id: WeightClassId
    frame_id: FrameId
    id: WheelId

    raw_features: WheelFeatures

    masked_features: WheelFeatures | None
    compression: float | None

    data: WheelReadingData

    @classmethod
    def new(cls, frame: "Frame", bbx: WheelBBX) -> Self:
        return cls(
            weight_class_id=frame.weight_class_id,
            frame_id=frame.id,
            id=bbx.id,
            raw_features=bbx.as_features(),
            masked_features=None,
            compression=None,
            data=WheelReadingData(),
        )
