from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, status
from sqlalchemy import update

from api.dependencies import DBSession, TokenData
from api.models.user.reset_email import EmailValidateRequest, EmailValidateResponce
from common.models.user.otp import ValidateEmailOTP
from common.sql.scripts.getters import validate_otp
from common.sql.tables import UserTable
from common.types import UserId

router = APIRouter()


@router.post("/validate", status_code=200, operation_id="Validate Email Reset")
async def validate_email(
    user_id: Annotated[UserId, Path()],
    request: Annotated[EmailValidateRequest, Body()],
    session_maker: DBSession,
    token_data: TokenData,
) -> EmailValidateResponce:

    if user_id != token_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this user")

    async with session_maker() as session:
        otp = await validate_otp(session, ValidateEmailOTP, request.code, token_data.id, delete_after=True)

        if otp is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Expired or invalid code")

        await session.execute(update(UserTable).where(UserTable.id == otp.user_id).values(email=otp.data.new_email, email_verified=True))

        await session.commit()

    return EmailValidateResponce()
