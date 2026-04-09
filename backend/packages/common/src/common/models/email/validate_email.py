from typing import Literal, Self

from common.models.email import EmailMessage, EmailType, Recipient


def _build_content(otp: str) -> str:
    return f"Your email validation code: <b>{otp}</b>"


class ValidateEmailMessage(EmailMessage):
    type: Literal[EmailType.VALIDATE_EMAIL] = EmailType.VALIDATE_EMAIL
    subject: str = "Validate Your Email"

    @classmethod
    def new(cls, email_to: str, otp: str) -> Self:
        return cls(
            to=Recipient(
                email=email_to,
            ),
            content=_build_content(otp),
        )
