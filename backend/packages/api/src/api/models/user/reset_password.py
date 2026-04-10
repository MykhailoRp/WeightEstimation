from pydantic import BaseModel


class PasswordResetRequest(BaseModel):
    email: str


class PasswordSetRequest(BaseModel):
    code: str
    new_password: str


class PasswordSetResponce(BaseModel):
    pass
