from datetime import datetime
from typing import Self

from pydantic import BaseModel

from common.models.user.otp import OTP, OTPType
from common.types import UserId


class OTPResponse(BaseModel):
    type: OTPType
    user_id: UserId
    expire_at: datetime

    @classmethod
    def new(cls, otp: OTP, /) -> Self:
        return cls(
            type=otp.type,
            user_id=otp.user_id,
            expire_at=otp.expire_at,
        )
