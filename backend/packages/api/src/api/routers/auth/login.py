from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import DBSession, SecretsManager
from api.models.auth import LoginResponse
from common.sql.scripts.getters import get_user_with_role
from common.sql.tables.user.session import SessionTable

router = APIRouter()


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session_maker: DBSession,
    secrets_manager: SecretsManager,
) -> LoginResponse:
    async with session_maker() as session:
        user = await get_user_with_role(session, email=form_data.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not secrets_manager.check_hash(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password or email")

    new_token = secrets_manager.encode_token(user=user)
    new_session = secrets_manager.mint_session(user=user)

    async with session_maker() as session:
        session.add(SessionTable.new(new_session))
        await session.commit()

    return LoginResponse(jwt_token=new_token, session=new_session.token)
