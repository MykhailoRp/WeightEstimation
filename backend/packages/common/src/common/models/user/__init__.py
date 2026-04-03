from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel

from common.types import UserId


class UserRole(StrEnum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"


class User(BaseModel):
    id: UserId
    email: str
    email_verified: bool
    password_hash: str
    created_at: datetime


class UserWithRole(User):
    role: set[UserRole]

    def is_(self, *r: list[UserRole]) -> bool:
        return len(set(r).union(self.role)) > 0

    @classmethod
    def new(cls, u: User, *, is_admin: bool, is_customer: bool) -> Self:
        r = set()
        if is_admin:
            r.add(UserRole.ADMIN)
        if is_customer:
            r.add(UserRole.CUSTOMER)
        return cls(
            id=u.id,
            email=u.email,
            email_verified=u.email_verified,
            password_hash=u.password_hash,
            created_at=u.created_at,
            role=r,
        )
