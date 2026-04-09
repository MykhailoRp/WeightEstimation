import uuid
from datetime import UTC, datetime
from enum import StrEnum

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


def new_user(email: str, password_hash: str) -> User:
    return User(
        id=uuid.uuid4(),
        email=email,
        email_verified=False,
        password_hash=password_hash,
        created_at=datetime.now(tz=UTC),
    )


class UserWithRole(User):
    role: set[UserRole]

    def is_(self, *r: list[UserRole]) -> bool:
        return len(set(r).union(self.role)) > 0


def new_user_with_role(u: User, *, is_admin: bool, is_customer: bool) -> UserWithRole:
    r = set()
    if is_admin:
        r.add(UserRole.ADMIN)
    if is_customer:
        r.add(UserRole.CUSTOMER)
    return UserWithRole(
        id=u.id,
        email=u.email,
        email_verified=u.email_verified,
        password_hash=u.password_hash,
        created_at=u.created_at,
        role=r,
    )
