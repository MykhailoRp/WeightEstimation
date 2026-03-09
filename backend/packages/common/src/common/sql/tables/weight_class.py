from datetime import datetime
from typing import TYPE_CHECKING, Self

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.weight_class import WeightClassification, WeightClassResult, WeightClassStatus
from common.sql.tables import Base
from common.types import S3Key, WeightClassId

if TYPE_CHECKING:
    from common.sql.tables.frame import FrameTable
    from common.sql.tables.wheel_feature import WheelFeatureTable


class WeightClassificationTable(Base):
    __tablename__ = "weight_classifications"

    id: Mapped[WeightClassId] = mapped_column(primary_key=True)
    # user_id: Mapped[UserId] = mapped_column(ForeignKey(UserTable.id)) # TODO: enable after implementing users
    status: Mapped[WeightClassStatus]
    result: Mapped[WeightClassResult | None]

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(True))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(True), server_onupdate=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(True))

    video_key: Mapped[S3Key]

    processing_cost: Mapped[float | None]

    # relationships
    # created_by: Mapped[UserTable] = relationship(back_populates="weight_classifications")
    frames: Mapped[list["FrameTable"]] = relationship(back_populates="weight_classification")
    wheel_features: Mapped[list["WheelFeatureTable"]] = relationship(back_populates="weight_classification")

    def m(self) -> WeightClassification:
        return WeightClassification(
            id=self.id,
            status=self.status,
            result=self.result,
            created_at=self.created_at,
            updated_at=self.updated_at,
            finished_at=self.finished_at,
            video_key=self.video_key,
            processing_cost=self.processing_cost,
        )

    @classmethod
    def new(cls, model: WeightClassification, /) -> Self:
        return cls(
            id=model.id,
            status=model.status,
            result=model.result,
            created_at=model.created_at,
            updated_at=model.updated_at,
            finished_at=model.finished_at,
            video_key=model.video_key,
            processing_cost=model.processing_cost,
        )
