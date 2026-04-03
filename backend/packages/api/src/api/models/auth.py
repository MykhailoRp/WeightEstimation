from pydantic import BaseModel


class LoginResponse(BaseModel):
    jwt_token: str
    session: str


class LogoutRequest(BaseModel):
    session: str


class LogoutResponse(BaseModel):
    pass
