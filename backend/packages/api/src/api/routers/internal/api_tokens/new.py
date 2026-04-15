from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from api.dependencies import DBSession, SecretsManager, TokenData
from api.models.api_token import ApiTokenDetailsResponse, NewApiTokenRequest
from common.models.user import UserRole
from common.sql.scripts.api_token import count_api_tokens
from common.sql.tables import ApiTokenTable

router = APIRouter()


@router.post("/", status_code=200, operation_id="Create New Api Token")
async def new_token(
    request: Annotated[NewApiTokenRequest, Body()],
    session_maker: DBSession,
    secrets_manager: SecretsManager,
    token_data: TokenData,
) -> ApiTokenDetailsResponse:

    if request.customer_id != token_data.id and not token_data.is_(UserRole.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this customer")

    new_token = secrets_manager.mint_api_token(customer_id=request.customer_id)

    async with session_maker() as session:
        count = await count_api_tokens(session, customer_ids=[request.customer_id])
        if count >= 5:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Max api token count is 5")

        session.add(ApiTokenTable.new(new_token))
        await session.commit()

    return new_token
