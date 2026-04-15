from pydantic import BaseModel

from common.types import UserId


class Admin(BaseModel):
    id: UserId
    promoted_by_id: UserId | None
