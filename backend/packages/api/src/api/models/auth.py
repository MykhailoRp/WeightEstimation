from typing import Literal

from pydantic import BaseModel


class LoginResponse(BaseModel):
    token_type: Literal["bearer"] = "bearer"
    access_token: str
    session: str


class LogoutRequest(BaseModel):
    session: str


class LogoutResponse(BaseModel):
    pass
