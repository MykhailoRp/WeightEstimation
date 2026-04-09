from pydantic import BaseModel

from common.types import UserId


class NewUserRequest(BaseModel):
    email: str
    password: str


class ValidateUserRequest(BaseModel):
    user_id: UserId
    code: str


class ValidateUserResponse(BaseModel):
    pass
