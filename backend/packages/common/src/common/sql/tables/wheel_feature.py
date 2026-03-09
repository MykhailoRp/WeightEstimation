from typing import Any, Self

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.bounding_box import BoundingBox
from common.models.weight_class.wheel_feature import WheelFeature, WheelFeatureData
from common.sql.tables.base import Base
from common.sql.tables.frame import FrameTable
from common.sql.types.pydantic_type import PydanticJSON
from common.types import FrameId, WeightClassId, WheelId


class WheelFeatureTable(Base):
    __tablename__ = "wheel_features"

    weight_class_id: Mapped[WeightClassId] = mapped_column(ForeignKey(FrameTable.weight_class_id), primary_key=True)
    frame_id: Mapped[FrameId] = mapped_column(ForeignKey(FrameTable.id), primary_key=True)
    id: Mapped[WheelId] = mapped_column(primary_key=True)

    rim: Mapped[BoundingBox] = mapped_column(PydanticJSON(BoundingBox))
    tire: Mapped[BoundingBox] = mapped_column(PydanticJSON(BoundingBox))

    data: Mapped[WheelFeatureData | None] = mapped_column(PydanticJSON(WheelFeatureData))

    __table_args__: tuple[Any, ...] = (
        ForeignKeyConstraint(
            [frame_id, weight_class_id],
            [FrameTable.id, FrameTable.weight_class_id],
        ),
    )

    # relationships
    frame: Mapped[FrameTable] = relationship(back_populates="wheel_features", foreign_keys=[frame_id, weight_class_id])

    def m(self) -> WheelFeature:
        return WheelFeature(
            id=self.id,
            frame_id=self.frame_id,
            weight_class_id=self.weight_class_id,
            rim=self.rim,
            tire=self.tire,
            data=self.data,
        )

    @classmethod
    def new(cls, model: WheelFeature, /) -> Self:
        return cls(
            id=model.id,
            frame_id=model.frame_id,
            weight_class_id=model.weight_class_id,
            rim=model.rim,
            tire=model.tire,
            data=model.data,
        )
