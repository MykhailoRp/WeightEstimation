from typing import TYPE_CHECKING, Self

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.weight_class.frame import Frame
from common.sql.tables.base import Base
from common.sql.tables.weight_class import WeightClassificationTable
from common.types import FrameId, S3Key, WeightClassId

if TYPE_CHECKING:
    from common.sql.tables.wheel_reading import WheelReadingTable


class FrameTable(Base):
    __tablename__ = "frames"

    weight_class_id: Mapped[WeightClassId] = mapped_column(ForeignKey(WeightClassificationTable.id), primary_key=True)
    id: Mapped[FrameId] = mapped_column(primary_key=True)

    s3_key: Mapped[S3Key]

    # relationships
    weight_classification: Mapped[WeightClassificationTable] = relationship(back_populates="frames")
    wheel_readings: Mapped[list["WheelReadingTable"]] = relationship(
        back_populates="frame",
        foreign_keys="WheelReadingTable.frame_id, WheelReadingTable.weight_class_id",
    )

    def m(self) -> Frame:
        return Frame(
            id=self.id,
            weight_class_id=self.weight_class_id,
            s3_key=self.s3_key,
        )

    @classmethod
    def new(cls, model: Frame, /) -> Self:
        return cls(
            id=model.id,
            weight_class_id=model.weight_class_id,
            s3_key=model.s3_key,
        )
