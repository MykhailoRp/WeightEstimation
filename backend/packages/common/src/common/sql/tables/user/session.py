from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.sql.tables.base import Base
from common.sql.tables.user import UserTable
from common.types import UserId


class SessionTable(Base):
    __tablename__ = "sessions"

    token: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[UserId] = mapped_column(ForeignKey(UserTable.id))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    expire_at: Mapped[datetime]

    # relationships
    user: Mapped[UserTable] = relationship(back_populates="sessions")
