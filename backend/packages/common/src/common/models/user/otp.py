import string
from abc import ABC, abstractmethod
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import BaseModel, Field

from common.types import UserId
from common.utils import secrets_choice


class _OPTGenerator(ABC):
    @staticmethod
    @abstractmethod
    def get_password() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_expire_at() -> datetime:
        pass


class _ValidateEmailGenerator(_OPTGenerator):
    @staticmethod
    def get_password() -> str:
        return secrets_choice(string.ascii_uppercase + string.digits, 6)

    @staticmethod
    def get_expire_at() -> datetime:
        return datetime.now(tz=UTC) + timedelta(minutes=30)


class _ValidateUserGenerator(_ValidateEmailGenerator):
    pass


class _ResetPasswordGenerator(_OPTGenerator):
    @staticmethod
    def get_password() -> str:
        return secrets_choice(string.ascii_uppercase + string.digits, 12)

    @staticmethod
    def get_expire_at() -> datetime:
        return datetime.now(tz=UTC) + timedelta(minutes=30)


class OTPType(StrEnum):
    VALIDATE_USER = "VALIDATE_USER"
    VALIDATE_EMAIL = "VALIDATE_EMAIL"
    RESET_PASSWORD = "RESET_PASSWORD"


class _OTPData(BaseModel):
    type: OTPType


class ValidateUserOTPData(_OTPData):
    type: Literal[OTPType.VALIDATE_USER] = OTPType.VALIDATE_USER


class ValidateEmailOTPData(_OTPData):
    type: Literal[OTPType.VALIDATE_EMAIL] = OTPType.VALIDATE_EMAIL
    new_email: str


class ResetPasswordOTPData(_OTPData):
    type: Literal[OTPType.RESET_PASSWORD] = OTPType.RESET_PASSWORD


OTPData = Annotated[ValidateUserOTPData | ValidateEmailOTPData | ResetPasswordOTPData, Field(discriminator="type")]


class OTP(ABC, BaseModel):
    user_id: UserId
    type: OTPType
    password: str
    data: OTPData
    expire_at: datetime


class ValidateUserOTP(OTP):
    type: Literal[OTPType.VALIDATE_USER] = OTPType.VALIDATE_USER
    data: ValidateUserOTPData

    @classmethod
    def new(cls, user_id: UserId) -> Self:
        return cls(
            user_id=user_id,
            password=_ValidateUserGenerator.get_password(),
            data=ValidateUserOTPData(),
            expire_at=_ValidateUserGenerator.get_expire_at(),
        )


class ValidateEmailOTP(OTP):
    type: Literal[OTPType.VALIDATE_EMAIL] = OTPType.VALIDATE_EMAIL
    data: ValidateEmailOTPData

    @classmethod
    def new(cls, user_id: UserId, new_email: str) -> Self:
        return cls(
            user_id=user_id,
            password=_ValidateEmailGenerator.get_password(),
            data=ValidateEmailOTPData(new_email=new_email),
            expire_at=_ValidateEmailGenerator.get_expire_at(),
        )


class ResetPasswordOTP(OTP):
    type: Literal[OTPType.RESET_PASSWORD] = OTPType.RESET_PASSWORD
    data: ResetPasswordOTPData

    @classmethod
    def new(cls, user_id: UserId) -> Self:
        return cls(
            user_id=user_id,
            password=_ResetPasswordGenerator.get_password(),
            data=ResetPasswordOTPData(),
            expire_at=_ResetPasswordGenerator.get_expire_at(),
        )


AnyOTP = Annotated[ValidateUserOTP | ValidateEmailOTP | ResetPasswordOTP, Field(discriminator="type")]
