from datetime import datetime
from typing import Self

from pydantic import BaseModel

from common.models.user.otp import OTP, OTPType


class OTPResponse(BaseModel):
    type: OTPType
    expire_at: datetime

    @classmethod
    def new(cls, otp: OTP, /) -> Self:
        return cls(
            type=otp.type,
            expire_at=otp.expire_at,
        )
