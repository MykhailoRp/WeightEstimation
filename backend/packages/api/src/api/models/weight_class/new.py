import uuid
from collections.abc import Callable
from datetime import UTC, datetime

from pydantic import BaseModel

from common.models.weight_class import WeightClassification, WeightClassResult, WeightClassStatus
from common.types import FileId, S3Key, UserId, WeightClassId


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
