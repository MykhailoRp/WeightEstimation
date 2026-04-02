from typing import Self

from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.weight_class.wheel_reading import WheelFeatures, WheelReading, WheelReadingData
from common.sql.tables.base import Base
from common.sql.tables.customer.weight_class.frame import FrameTable
from common.sql.types.pydantic_type import PydanticJSONB
from common.types import FrameId, WeightClassId, WheelId


class WheelReadingTable(Base):
    __tablename__ = "wheel_readings"

    weight_class_id: Mapped[WeightClassId] = mapped_column(primary_key=True)
    frame_id: Mapped[FrameId] = mapped_column(primary_key=True)
    id: Mapped[WheelId] = mapped_column(primary_key=True)

    raw_features: Mapped[WheelFeatures] = mapped_column(PydanticJSONB(WheelFeatures))

    masked_features: Mapped[WheelFeatures | None] = mapped_column(PydanticJSONB(WheelFeatures))
    compression: Mapped[float | None]

    data: Mapped[WheelReadingData] = mapped_column(PydanticJSONB(WheelReadingData))

    __table_args__ = (
        ForeignKeyConstraint(
            [frame_id, weight_class_id],
            [FrameTable.id, FrameTable.weight_class_id],
        ),
    )

    # relationships
    frame: Mapped[FrameTable] = relationship(back_populates="wheel_readings", foreign_keys=[frame_id, weight_class_id])

    def m(self) -> WheelReading:
        return WheelReading(
            id=self.id,
            frame_id=self.frame_id,
            weight_class_id=self.weight_class_id,
            raw_features=self.raw_features,
            masked_features=self.masked_features,
            compression=self.compression,
            data=self.data,
        )

    @classmethod
    def new(cls, model: WheelReading, /) -> Self:
        return cls(
            id=model.id,
            frame_id=model.frame_id,
            weight_class_id=model.weight_class_id,
            raw_features=model.raw_features,
            masked_features=model.masked_features,
            compression=model.compression,
            data=model.data,
        )
