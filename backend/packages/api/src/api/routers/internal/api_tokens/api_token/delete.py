from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from api.dependencies import DBSession, TokenData
from api.models.api_token import ApiTokenDetailsResponse
from common.models.user import UserRole
from common.sql.scripts.api_token import delete_token as delete_token_script
from common.types import ApiTokenStr

router = APIRouter()


@router.delete("/", status_code=200, operation_id="Delete Api Token")
async def delete_token(
    token: Annotated[ApiTokenStr, Query()],
    session_maker: DBSession,
    token_data: TokenData,
) -> ApiTokenDetailsResponse:
    async with session_maker() as session:
        deleted_token = await delete_token_script(session, token=token, customer_id=None if token_data.is_(UserRole.ADMIN) else token_data.id)

        if deleted_token is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")

        await session.commit()

    return deleted_token
