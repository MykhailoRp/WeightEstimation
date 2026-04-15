from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from api.dependencies import DBSession
from api.models.otp import OTPResponse
from api.models.user.reset_password import PasswordResetRequest
from common.kafka.messages.email import EmailSend
from common.kafka.topics import EmailSendTopic
from common.models.email.reset_password import ResetPasswordMessage
from common.models.user.otp import ResetPasswordOTP
from common.sql.scripts.user import get_user_with_role
from common.sql.tables.user.otp import OTPTable, insert_otp

router = APIRouter()


@router.post("/", status_code=200, operation_id="Request Password Reset")
async def reset_password(
    request: Annotated[PasswordResetRequest, Body()],
    session_maker: DBSession,
) -> OTPResponse:

    async with session_maker() as session:
        user = await get_user_with_role(session, email=request.email)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        otp = ResetPasswordOTP.new(user_id=user.id)
        letter = ResetPasswordMessage.new(email_to=user.email, otp=otp.password)

        await insert_otp(session, OTPTable.new(otp))
        await session.commit()

    await EmailSendTopic.send(
        key=EmailSend.key(),
        value=letter.model_dump_json(),
    )

    return OTPResponse.new(otp)
