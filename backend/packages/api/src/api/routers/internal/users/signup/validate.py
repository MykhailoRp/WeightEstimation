from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy import update

from api.dependencies import DBSession
from api.models.user.signup import ValidateUserRequest, ValidateUserResponse
from common.models.customer import Customer
from common.models.user.otp import ValidateUserOTP
from common.sql.scripts.getters import validate_otp
from common.sql.tables import CustomerTable, UserTable

router = APIRouter()


@router.post("/validate", status_code=200, operation_id="Validate New User")
async def validate_new_user(
    request: Annotated[ValidateUserRequest, Body()],
    session_maker: DBSession,
) -> ValidateUserResponse:

    async with session_maker() as session:
        otp = await validate_otp(session, ValidateUserOTP, request.code, request.user_id, delete_after=True)

        if otp is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Expired or invalid code")

        session.add(CustomerTable.new(Customer.new(otp.user_id)))
        await session.execute(update(UserTable).where(UserTable.id == request.user_id).values(email_verified=True))

        await session.commit()

    return ValidateUserResponse()
