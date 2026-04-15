from datetime import datetime
from typing import TYPE_CHECKING, Self

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.weight_class import WeightClassification, WeightClassResult, WeightClassStatus
from common.sql.tables import Base
from common.sql.tables.customer import CustomerTable
from common.types import S3Key, UserId, WeightClassId

if TYPE_CHECKING:
    from common.sql.tables.customer.weight_class.frame import FrameTable
    from common.sql.tables.customer.weight_class.wheel_aggregation import WheelAggregationTable


class WeightClassificationTable(Base):
    __tablename__ = "weight_classifications"

    id: Mapped[WeightClassId] = mapped_column(primary_key=True)
    vehicle_identifier: Mapped[str]
    customer_id: Mapped[UserId] = mapped_column(ForeignKey(CustomerTable.id, name="customer_fk"))
    status: Mapped[WeightClassStatus]
    assigned: Mapped[WeightClassResult]
    result: Mapped[WeightClassResult | None]

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(True))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(True), server_onupdate=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(True))

    video_key: Mapped[S3Key]

    processing_cost: Mapped[float | None]

    # relationships
    customer: Mapped[CustomerTable] = relationship(back_populates="weight_classifications")

    frames: Mapped[list["FrameTable"]] = relationship(back_populates="weight_classification")
    wheel_aggregations: Mapped[list["WheelAggregationTable"]] = relationship(back_populates="weight_classification")

    def m(self) -> WeightClassification:
        return WeightClassification(
            id=self.id,
            customer_id=self.customer_id,
            vehicle_identifier=self.vehicle_identifier,
            status=self.status,
            assigned=self.assigned,
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
            customer_id=model.customer_id,
            vehicle_identifier=model.vehicle_identifier,
            status=model.status,
            assigned=model.assigned,
            result=model.result,
            created_at=model.created_at,
            updated_at=model.updated_at,
            finished_at=model.finished_at,
            video_key=model.video_key,
            processing_cost=model.processing_cost,
        )
