from datetime import datetime
from typing import Self

from pydantic import BaseModel

from common.models.weight_class.weight_class import WeightClassification, WeightClassResult, WeightClassStatus
from common.types import S3Url, UserId, WeightClassId


class WeightClassificationResponse(BaseModel):
    id: WeightClassId
    vehicle_identifier: str
    customer_id: UserId
    status: WeightClassStatus
    assigned: WeightClassResult
    result: WeightClassResult | None

    created_at: datetime
    updated_at: datetime
    finished_at: datetime | None

    video_url: S3Url

    processing_cost: float | None

    @classmethod
    def new(cls, m: WeightClassification, signed_url: S3Url) -> Self:
        return cls(
            id=m.id,
            vehicle_identifier=m.vehicle_identifier,
            customer_id=m.customer_id,
            status=m.status,
            assigned=m.assigned,
            result=m.result,
            created_at=m.created_at,
            updated_at=m.updated_at,
            finished_at=m.finished_at,
            video_url=signed_url,
            processing_cost=m.processing_cost,
        )
