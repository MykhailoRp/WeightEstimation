from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.sql.tables.base import Base
from common.types import UserId

if TYPE_CHECKING:
    from common.sql.tables import WeightClassificationTable


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[UserId] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    email_verified: Mapped[bool] = mapped_column(server_default=text("false"))
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=text("NOW()"))

    # relationships
    weight_classifications: Mapped[list["WeightClassificationTable"]] = relationship(back_populates="created_by")
