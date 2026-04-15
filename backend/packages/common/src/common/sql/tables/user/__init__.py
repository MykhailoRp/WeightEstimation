from datetime import datetime
from typing import TYPE_CHECKING, Self

from sqlalchemy import TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.user import User
from common.sql.tables.base import Base
from common.types import UserId

if TYPE_CHECKING:
    from common.sql.tables.admin import AdminTable
    from common.sql.tables.customer import CustomerTable
    from common.sql.tables.user.otp import OTPTable
    from common.sql.tables.user.session import SessionTable


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[UserId] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    email_verified: Mapped[bool] = mapped_column(server_default=text("false"))
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(True), server_default=text("NOW()"))

    # relationships
    sessions: Mapped[list["SessionTable"]] = relationship(back_populates="user")
    one_time_passwords: Mapped[list["OTPTable"]] = relationship(back_populates="user")
    admin: Mapped["AdminTable"] = relationship(back_populates="user")
    customer: Mapped["CustomerTable"] = relationship(back_populates="user")

    @classmethod
    def new(cls, u: User, /) -> Self:
        return cls(
            id=u.id,
            email=u.email,
            email_verified=u.email_verified,
            password_hash=u.password_hash,
            created_at=u.created_at,
        )

    def m(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            email_verified=self.email_verified,
            password_hash=self.password_hash,
            created_at=self.created_at,
        )
