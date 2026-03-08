from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

from common.types import S3Key, WeightClassId


class WeightClassStatus(StrEnum):
    PENDING = "pending"
    FRAMES_SPLIT = "frames_split"
    MASKS_EXTRACTED = "masks_extracted"
    FEATURES_EXTRACTED = "features_extracted"
    COMPLETED = "completed"


class WeightClassResult(StrEnum):
    EMPTY = "empty"
    LOADED = "loaded"


class WeightClassification(BaseModel):
    id: WeightClassId
    # user_id: UserId  # TODO: enable after implementing users
    status: WeightClassStatus
    result: WeightClassResult | None

    created_at: datetime
    updated_at: datetime
    finished_at: datetime | None

    video_key: S3Key

    processing_cost: float | None
