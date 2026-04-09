from typing import Annotated

from fastapi import APIRouter, Body

from api.dependencies import DBSession, SecretsManager
from api.models.otp import OTPResponse
from api.models.user.signup import NewUserRequest
from common.kafka.messages.email import EmailSend
from common.kafka.topics import EmailSendTopic
from common.models.email.validate_email import ValidateEmailMessage
from common.models.user import new_user
from common.models.user.otp import ValidateUserOTP
from common.sql.tables.user import UserTable
from common.sql.tables.user.otp import OTPTable

router = APIRouter()


@router.post("/", status_code=200, operation_id="Create New User")
async def create_new_user(
    request: Annotated[NewUserRequest, Body()],
    session_maker: DBSession,
    secrets_manager: SecretsManager,
) -> OTPResponse:

    user = new_user(email=request.email, password_hash=secrets_manager.hash_pass(request.password))
    otp = ValidateUserOTP.new(user_id=user.id)
    letter = ValidateEmailMessage.new(email_to=user.email, otp=otp.password)

    async with session_maker() as session:
        session.add_all(
            [
                UserTable.new(user),
                OTPTable.new(otp),
            ],
        )
        await session.commit()

    await EmailSendTopic.send(
        key=EmailSend.key(),
        value=letter.model_dump_json(),
    )

    return OTPResponse.new(otp)
