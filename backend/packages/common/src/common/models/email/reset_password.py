from typing import Literal, Self

from common.models.email import EmailMessage, EmailType, Recipient


def _build_content(otp: str) -> str:
    return f"Your reset password code: <b>{otp}</b>"


class ResetPasswordMessage(EmailMessage):
    type: Literal[EmailType.RESET_PASSWORD] = EmailType.RESET_PASSWORD
    subject: str = "Reset Password Request"

    @classmethod
    def new(cls, email_to: str, otp: str) -> Self:
        return cls(
            to=Recipient(
                email=email_to,
            ),
            content=_build_content(otp),
        )
