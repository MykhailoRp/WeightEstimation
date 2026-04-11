from datetime import datetime

from pydantic import BaseModel

from common.types import UserId


class ApiTokenData(BaseModel):
    customer_id: UserId
    t: int


class ApiToken(BaseModel):
    token: str
    customer_id: UserId

    created_at: datetime
