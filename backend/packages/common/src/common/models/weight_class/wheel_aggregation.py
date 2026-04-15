from pydantic import BaseModel

from common.types import WeightClassId, WheelId


class WheelAggregation(BaseModel):
    weight_class_id: WeightClassId
    id: WheelId

    median: float
    std: float
