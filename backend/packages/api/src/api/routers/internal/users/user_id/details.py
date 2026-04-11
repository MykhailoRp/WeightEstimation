from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from api.dependencies import DBSession, TokenData
from api.models.user import UserDetailsResponse
from common.models.user import UserRole
from common.sql.scripts.getters import get_user_with_role
from common.types import UserId

router = APIRouter()


@router.get("/", status_code=200, operation_id="Get User Details")
async def get_user(
    user_id: Annotated[UserId, Path()],
    session_maker: DBSession,
    token_data: TokenData,
) -> UserDetailsResponse:

    if user_id != token_data.id and not token_data.is_(UserRole.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this user")

    async with session_maker() as session:
        user = await get_user_with_role(session, id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserDetailsResponse.new(user)
