from datetime import datetime
from typing import Self

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.user.session import Session
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

    @classmethod
    def new(cls, m: Session, /) -> Self:
        return cls(
            token=m.token,
            user_id=m.user_id,
            created_at=m.created_at,
            expire_at=m.expire_at,
        )

    def m(self) -> Session:
        return Session(
            token=self.token,
            user_id=self.user_id,
            created_at=self.created_at,
            expire_at=self.expire_at,
        )
