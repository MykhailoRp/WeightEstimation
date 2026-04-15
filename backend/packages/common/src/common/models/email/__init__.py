from enum import StrEnum

from pydantic import BaseModel


class EmailType(StrEnum):
    VALIDATE_EMAIL = "VALIDATE_EMAIL"
    RESET_PASSWORD = "RESET_PASSWORD"


class Recipient(BaseModel):
    name: str | None = None
    email: str


class EmailMessage(BaseModel):
    type: EmailType

    to: Recipient

    subject: str
    content: str
