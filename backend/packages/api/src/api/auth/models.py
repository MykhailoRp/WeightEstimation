from datetime import UTC, datetime, timedelta
from typing import Self

from pydantic import BaseModel

from common.models.user import UserRole, UserWithRole
from common.types import UserId


class TokenData(BaseModel):
    id: UserId
    email: str
    role: set[UserRole]

    def is_(self, *r: UserRole) -> bool:
        return len(set(r).union(self.role)) > 0

    @classmethod
    def new(cls, u: UserWithRole, /) -> Self:
        return cls(
            id=u.id,
            email=u.email,
            role=u.role,
        )


class Token(BaseModel):
    expire_at: datetime
    data: TokenData

    @classmethod
    def new(cls, user: UserWithRole, expire_in_minutes: int) -> Self:
        return cls(
            expire_at=datetime.now(tz=UTC) + timedelta(minutes=expire_in_minutes),
            data=TokenData.new(user),
        )
