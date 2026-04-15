from pydantic import BaseModel


class EmailResetRequest(BaseModel):
    new_email: str


class EmailValidateRequest(BaseModel):
    code: str


class EmailValidateResponce(BaseModel):
    pass
