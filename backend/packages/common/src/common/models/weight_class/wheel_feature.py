from pydantic import BaseModel

from common.models.weight_class.frame import WheelBBX
from common.types import FrameId, S3Key, WeightClassId


class WheelFeatureData(BaseModel):
    rim_mask_key: S3Key
    tire_mask_key: S3Key

    model_name: str


class WheelFeature(WheelBBX):
    weight_class_id: WeightClassId
    frame_id: FrameId

    data: WheelFeatureData | None

    # TODO: add feature calculations here
