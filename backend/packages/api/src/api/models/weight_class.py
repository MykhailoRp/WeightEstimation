import uuid
from datetime import UTC, datetime

from pydantic import BaseModel

from common.models.weight_class import WeightClassification, WeightClassStatus
from common.types import UserId, WeightClassId


class NewWeightClassification(BaseModel):
    video_url: str

    def create(self, user_id: UserId) -> WeightClassification:

        now = datetime.now(tz=UTC)

        return WeightClassification(
            id=WeightClassId(uuid.uuid4()),
            user_id=user_id,
            status=WeightClassStatus.PENDING,
            result=None,
            created_at=now,
            updated_at=now,
            finished_at=None,
            video_url=self.video_url,
            processing_cost=None,
        )
