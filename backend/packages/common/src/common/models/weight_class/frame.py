from pydantic import BaseModel

from common.types import FrameId, S3Key, WeightClassId


class Frame(BaseModel):
    id: FrameId
    weight_class_id: WeightClassId

    s3_key: S3Key
