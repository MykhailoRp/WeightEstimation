from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from api.dependencies import DBSession
from api.models.user.signup import ValidateUserRequest
from common.models.user.otp import ValidateUserOTP
from common.sql.scripts.getters import validate_otp

router = APIRouter()


@router.post("/validate", status_code=200, operation_id="Validate New User")
async def create_new_user(
    request: Annotated[ValidateUserRequest, Body()],
    session_maker: DBSession,
) -> None:

    async with session_maker() as session:
        otp = validate_otp(session, ValidateUserOTP, request.code, request.user_id, delete_after=True)

        if otp is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Expired or invalid code")

        await session.commit()
