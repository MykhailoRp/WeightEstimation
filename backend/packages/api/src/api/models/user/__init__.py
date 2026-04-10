from datetime import datetime
from typing import Self

from pydantic import BaseModel

from common.models.user import User
from common.types import UserId


class UserDetailsResponse(BaseModel):
    id: UserId
    email: str
    email_verified: bool
    created_at: datetime

    @classmethod
    def new(cls, m: User, /) -> Self:
        return cls(
            id=m.id,
            email=m.email,
            email_verified=m.email_verified,
            created_at=m.created_at,
        )
