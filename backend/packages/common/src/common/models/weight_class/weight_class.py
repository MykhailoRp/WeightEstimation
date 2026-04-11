from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

from common.types import S3Key, UserId, WeightClassId


class WeightClassStatus(StrEnum):
    PENDING = "PENDING"
    FRAMES_SPLIT = "FRAMES_SPLIT"
    MASKS_EXTRACTED = "MASKS_EXTRACTED"
    FEATURES_EXTRACTED = "FEATURES_EXTRACTED"
    COMPLETED = "COMPLETED"


class WeightClassResult(StrEnum):
    EMPTY = "EMPTY"
    LOADED = "LOADED"


class WeightClassification(BaseModel):
    id: WeightClassId
    vehicle_identifier: str
    customer_id: UserId
    status: WeightClassStatus
    assigned: WeightClassResult
    result: WeightClassResult | None

    created_at: datetime
    updated_at: datetime
    finished_at: datetime | None

    video_key: S3Key

    processing_cost: float | None
