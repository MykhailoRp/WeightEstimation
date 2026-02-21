from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from common.sql.tables.base import Base
from common.types import UserId


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[UserId] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    email_verified: Mapped[bool] = mapped_column(server_default=text("false"))
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=text("NOW()"))
