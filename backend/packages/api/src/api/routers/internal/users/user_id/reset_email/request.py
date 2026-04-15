from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, status

from api.dependencies import DBSession, TokenData
from api.models.otp import OTPResponse
from api.models.user.reset_email import EmailResetRequest
from common.kafka.messages.email import EmailSend
from common.kafka.topics import EmailSendTopic
from common.models.email.validate_email import ValidateEmailMessage
from common.models.user.otp import ValidateEmailOTP
from common.sql.tables.user.otp import OTPTable, insert_otp
from common.types import UserId

router = APIRouter()


@router.post("/", status_code=200, operation_id="Request Email Reset")
async def reset_email(
    user_id: Annotated[UserId, Path()],
    request: Annotated[EmailResetRequest, Body()],
    session_maker: DBSession,
    token_data: TokenData,
) -> OTPResponse:

    if user_id != token_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this user")

    otp = ValidateEmailOTP.new(user_id=token_data.id, new_email=request.new_email)
    letter = ValidateEmailMessage.new(email_to=request.new_email, otp=otp.password)

    async with session_maker() as session:
        await insert_otp(session, OTPTable.new(otp))
        await session.commit()

    await EmailSendTopic.send(
        key=EmailSend.key(),
        value=letter.model_dump_json(),
    )

    return OTPResponse.new(otp)
