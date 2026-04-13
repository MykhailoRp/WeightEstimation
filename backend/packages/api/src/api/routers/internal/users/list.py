from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from api.dependencies import DBSession, TokenData
from api.models.user import UserListRequest, UserListResponse
from common.models.user import UserRole
from common.sql.scripts.user import count_users
from common.sql.scripts.user import get_users as get_users_script

router = APIRouter()


@router.get("/", status_code=200, operation_id="Get Users List")
async def get_users(
    query: Annotated[UserListRequest, Query()],
    session_maker: DBSession,
    token_data: TokenData,
) -> UserListResponse:

    if not token_data.is_(UserRole.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    async with session_maker() as session:
        users = await get_users_script(
            session,
            email_like=query.email_like,
            roles=query.roles,
            limit=query.size,
            offset=query.offset,
        )
        total = await count_users(
            session,
            email_like=query.email_like,
            roles=query.roles,
        )

    return UserListResponse.new(
        users,
        total,
    )
