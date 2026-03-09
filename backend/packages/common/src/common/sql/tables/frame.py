from typing import TYPE_CHECKING, Self

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.weight_class.frame import Frame, FrameStatus, WheelBBX
from common.sql.tables.base import Base
from common.sql.tables.weight_class import WeightClassificationTable
from common.sql.types.pydantic_type import PydanticJSON
from common.types import FrameId, S3Key, WeightClassId

if TYPE_CHECKING:
    from common.sql.tables.wheel_feature import WheelFeatureTable


class FrameTable(Base):
    __tablename__ = "frames"

    id: Mapped[FrameId] = mapped_column(primary_key=True)
    weight_class_id: Mapped[WeightClassId] = mapped_column(ForeignKey(WeightClassificationTable.id), primary_key=True)

    status: Mapped[FrameStatus]

    s3_key: Mapped[S3Key]

    wheel_bbxs: Mapped[list[WheelBBX]] = mapped_column(PydanticJSON(list[WheelBBX]))

    # relationships
    weight_classification: Mapped[WeightClassificationTable] = relationship(back_populates="frames")
    wheel_features: Mapped[list["WheelFeatureTable"]] = relationship(
        back_populates="frame",
        foreign_keys="WheelFeatureTable.frame_id, WheelFeatureTable.weight_class_id",
    )

    def m(self) -> Frame:
        return Frame(
            id=self.id,
            weight_class_id=self.weight_class_id,
            status=self.status,
            s3_key=self.s3_key,
            wheel_bbxs=self.wheel_bbxs,
        )

    @classmethod
    def new(cls, model: Frame, /) -> Self:
        return cls(
            id=model.id,
            weight_class_id=model.weight_class_id,
            status=model.status,
            s3_key=model.s3_key,
            wheel_bbxs=model.wheel_bbxs,
        )
