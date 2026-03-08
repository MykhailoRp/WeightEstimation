import uuid
from collections.abc import Callable
from datetime import UTC, datetime

from pydantic import BaseModel

from common.models.weight_class import WeightClassification, WeightClassStatus
from common.types import FileId, S3Key, UserId, WeightClassId


class NewWeightClassification(BaseModel):
    file_id: FileId

    def create(self, user_id: UserId, video_key: Callable[[WeightClassId], S3Key]) -> WeightClassification:

        now = datetime.now(tz=UTC)
        id_ = WeightClassId(uuid.uuid4())

        return WeightClassification(
            id=id_,
            # user_id=user_id,
            status=WeightClassStatus.PENDING,
            result=None,
            created_at=now,
            updated_at=now,
            finished_at=None,
            video_key=video_key(id_),
            processing_cost=None,
        )
