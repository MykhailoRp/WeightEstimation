from enum import StrEnum

from pydantic import BaseModel

from common.models.bounding_box import BoundingBox
from common.types import FrameId, TireId, WeightClassId


class TireBBX(BaseModel):
    id: TireId

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

    url: str

    tire_bbxs: list[TireBBX]
