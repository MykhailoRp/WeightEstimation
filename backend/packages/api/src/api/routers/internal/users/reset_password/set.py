from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy import update

from api.dependencies import DBSession, SecretsManager
from api.models.user.reset_password import PasswordSetRequest, PasswordSetResponce
from common.models.user.otp import ResetPasswordOTP
from common.sql.scripts.getters import validate_otp
from common.sql.tables import UserTable

router = APIRouter()


@router.post("/set", status_code=200, operation_id="Set New Password")
async def set_password(
    request: Annotated[PasswordSetRequest, Body()],
    session_maker: DBSession,
    secrets_manager: SecretsManager,
) -> PasswordSetResponce:

    async with session_maker() as session:
        otp = await validate_otp(session, ResetPasswordOTP, request.code, delete_after=True)

        if otp is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Expired or invalid code")

        await session.execute(
            update(UserTable).where(UserTable.id == otp.user_id).values(password_hash=secrets_manager.hash_pass(request.new_password)),
        )

        await session.commit()

    return PasswordSetResponce()
