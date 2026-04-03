from datetime import datetime

from pydantic import BaseModel

from common.types import UserId


class Session(BaseModel):
    token: str
    user_id: UserId
    created_at: datetime
    expire_at: datetime
