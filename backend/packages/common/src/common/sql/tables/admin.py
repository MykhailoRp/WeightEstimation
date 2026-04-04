from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.sql.tables.base import Base
from common.sql.tables.user import UserTable
from common.types import UserId


class AdminTable(Base):
    __tablename__ = "admins"

    id: Mapped[UserId] = mapped_column(ForeignKey(UserTable.id), primary_key=True)
    promoted_by_id: Mapped[UserId | None] = mapped_column(ForeignKey(id))

    # relationships
    user: Mapped[UserTable] = relationship(back_populates="admin")
    promoted_by: Mapped["AdminTable"] = relationship(back_populates="promoted", remote_side=[id])
    promoted: Mapped[list["AdminTable"]] = relationship(back_populates="promoted_by")
