from datetime import datetime
from typing import Self

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.user.otp import OTP, OTPData, OTPType
from common.sql.tables.base import Base
from common.sql.tables.user import UserTable
from common.sql.types.pydantic_type import PydanticJSONB
from common.types import UserId


class OTPTable(Base):
    __tablename__ = "one_time_passwords"

    user_id: Mapped[UserId] = mapped_column(ForeignKey(UserTable.id), primary_key=True)
    type: Mapped[OTPType] = mapped_column(primary_key=True)
    password: Mapped[str]
    data: Mapped[OTPData] = mapped_column(PydanticJSONB(OTPData))
    expire_at: Mapped[datetime] = mapped_column(TIMESTAMP(True))

    # relationships
    user: Mapped[UserTable] = relationship(back_populates="one_time_passwords")

    @classmethod
    def new(cls, m: OTP, /) -> Self:
        return cls(
            user_id=m.user_id,
            type=m.type,
            password=m.password,
            data=m.data,
            expire_at=m.expire_at,
        )

    def m(self) -> OTP:
        return OTP(
            user_id=self.user_id,
            type=self.type,
            password=self.password,
            data=self.data,
            expire_at=self.expire_at,
        )


async def insert_otp(session: AsyncSession, otp: OTPTable) -> None:
    await session.execute(insert(OTPTable).values(otp.dict()).on_conflict_do_update(index_elements=[OTPTable.user_id, OTPTable.type], set_=otp.dict()))
