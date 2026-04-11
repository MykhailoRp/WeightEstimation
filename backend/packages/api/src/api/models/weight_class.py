import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Self

from pydantic import BaseModel

from api.models.basic import ListResponse, Paginated
from common.models.weight_class.weight_class import WeightClassification, WeightClassResult, WeightClassStatus
from common.types import FileId, S3Key, S3Url, UserId, WeightClassId


class NewWeightClassification(BaseModel):
    customer_id: UserId

    file_id: FileId

    vehicle_identifier: str
    assigned: WeightClassResult

    def create(self, video_key: Callable[[WeightClassId], S3Key]) -> WeightClassification:

        now = datetime.now(tz=UTC)
        id_ = WeightClassId(uuid.uuid4())

        return WeightClassification(
            id=id_,
            customer_id=self.customer_id,
            vehicle_identifier=self.vehicle_identifier,
            status=WeightClassStatus.PENDING,
            assigned=self.assigned,
            result=None,
            created_at=now,
            updated_at=now,
            finished_at=None,
            video_key=video_key(id_),
            processing_cost=None,
        )


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


class WeightClassificationItem(BaseModel):
    id: WeightClassId
    vehicle_identifier: str
    customer_id: UserId
    status: WeightClassStatus
    result: WeightClassResult | None

    created_at: datetime
    updated_at: datetime
    finished_at: datetime | None

    processing_cost: float | None

    @classmethod
    def new(cls, m: WeightClassification) -> Self:
        return cls(
            id=m.id,
            vehicle_identifier=m.vehicle_identifier,
            customer_id=m.customer_id,
            status=m.status,
            result=m.result,
            created_at=m.created_at,
            updated_at=m.updated_at,
            finished_at=m.finished_at,
            processing_cost=m.processing_cost,
        )


class WeightClassificationListRequest(Paginated):
    customer_ids: list[UserId] | None = None


class WeightClassificationListResponse(ListResponse[WeightClassificationItem]):
    @classmethod
    def new(cls, m: list[WeightClassification], total_count: int) -> Self:
        return cls(
            items=[WeightClassificationItem.new(m_) for m_ in m],
            total_count=total_count,
        )
