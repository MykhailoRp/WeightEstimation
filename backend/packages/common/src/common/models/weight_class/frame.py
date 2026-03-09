from enum import StrEnum

from pydantic import BaseModel

from common.models.bounding_box import BoundingBox
from common.types import FrameId, S3Key, WeightClassId, WheelId


class WheelBBX(BaseModel):
    id: WheelId

    rim: BoundingBox
    tire: BoundingBox


class FrameStatus(StrEnum):
    NEW = "new"
    PROCESSED = "processed"
    FAILED = "failed"


class Frame(BaseModel):
    id: FrameId
    weight_class_id: WeightClassId

    status: FrameStatus

    s3_key: S3Key

    wheel_bbxs: list[WheelBBX]
