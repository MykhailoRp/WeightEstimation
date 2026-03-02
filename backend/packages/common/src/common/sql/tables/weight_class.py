from datetime import datetime
from typing import Self

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.weight_class import WeightClassification, WeightClassResult, WeightClassStatus
from common.sql.tables import Base, UserTable
from common.types import UserId, WeightClassId


class WeightClassificationTable(Base):
    __tablename__ = "weight_classifications"

    id: Mapped[WeightClassId] = mapped_column(primary_key=True)
    user_id: Mapped[UserId] = mapped_column(ForeignKey(UserTable.id))
    status: Mapped[WeightClassStatus]
    result: Mapped[WeightClassResult | None]

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime] = mapped_column(server_onupdate=func.now())
    finished_at: Mapped[datetime | None]

    video_url: Mapped[str]

    processing_cost: Mapped[float | None]

    # relationships
    created_by: Mapped[UserTable] = relationship(back_populates="weight_classifications")

    def m(self) -> WeightClassification:
        return WeightClassification(
            id=self.id,
            user_id=self.user_id,
            status=self.status,
            result=self.result,
            created_at=self.created_at,
            updated_at=self.updated_at,
            finished_at=self.finished_at,
            video_url=self.video_url,
            processing_cost=self.processing_cost,
        )

    @classmethod
    def new(cls, model: WeightClassification, /) -> Self:
        return cls(
            id=model.id,
            user_id=model.user_id,
            status=model.status,
            result=model.result,
            created_at=model.created_at,
            updated_at=model.updated_at,
            finished_at=model.finished_at,
            video_url=model.video_url,
            processing_cost=model.processing_cost,
        )
