from datetime import datetime
from typing import Self

from pydantic import BaseModel

from api.models.basic import ListResponse, Paginated
from common.models.user import UserRole, UserWithRole
from common.types import UserId


class UserDetailsResponse(BaseModel):
    id: UserId
    email: str
    email_verified: bool
    role: set[UserRole]
    created_at: datetime

    @classmethod
    def new(cls, m: UserWithRole, /) -> Self:
        return cls(
            id=m.id,
            email=m.email,
            email_verified=m.email_verified,
            role=m.role,
            created_at=m.created_at,
        )


class UserListRequest(Paginated):
    roles: set[UserRole] | None = None
    email_like: str | None = None


class UserListResponse(ListResponse[UserDetailsResponse]):
    @classmethod
    def new(cls, users: list[UserWithRole], total_count: int) -> Self:
        return cls(
            items=[UserDetailsResponse.new(u) for u in users],
            total_count=total_count,
        )
