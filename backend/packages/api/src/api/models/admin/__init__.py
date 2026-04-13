from typing import Self

from pydantic import BaseModel

from common.models.admin import Admin
from common.types import UserId


class NewAdminRequest(BaseModel):
    user_id: UserId


class AdminDetailsResponse(BaseModel):
    id: UserId
    promoted_by_id: UserId | None

    @classmethod
    def new(cls, m: Admin) -> Self:
        return cls(
            id=m.id,
            promoted_by_id=m.promoted_by_id,
        )


class DemoteAdminResponse(BaseModel):
    pass
