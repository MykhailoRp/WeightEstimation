from typing import Self

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.weight_class.wheel_aggregation import WheelAggregation
from common.sql.tables.base import Base
from common.sql.tables.weight_class import WeightClassificationTable
from common.types import WeightClassId, WheelId


class WheelAggregationTable(Base):
    __tablename__ = "wheel_aggregations"

    weight_class_id: Mapped[WeightClassId] = mapped_column(ForeignKey(WeightClassificationTable.id), primary_key=True)
    id: Mapped[WheelId] = mapped_column(primary_key=True)

    median: Mapped[float]
    std: Mapped[float]

    # relationships
    weight_classification: Mapped[WeightClassificationTable] = relationship(back_populates="wheel_aggregations")

    def m(self) -> WheelAggregation:
        return WheelAggregation(
            id=self.id,
            weight_class_id=self.weight_class_id,
            median=self.median,
            std=self.std,
        )

    @classmethod
    def new(cls, model: WheelAggregation, /) -> Self:
        return cls(
            id=model.id,
            weight_class_id=model.weight_class_id,
            median=model.median,
            std=model.std,
        )
