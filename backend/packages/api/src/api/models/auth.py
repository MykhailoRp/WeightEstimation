from typing import Literal

from pydantic import BaseModel

from api.auth.models import TokenData
from common.types import UserId


class _TokenData(BaseModel):
    token_type: Literal["bearer"] = "bearer"
    access_token: str
    data: TokenData


class LoginResponse(_TokenData):
    session: str


class LogoutRequest(BaseModel):
    session: str


class RefreshRequest(BaseModel):
    user_id: UserId
    session: str


class LogoutResponse(BaseModel):
    pass


class RefreshResponse(_TokenData):
    pass
