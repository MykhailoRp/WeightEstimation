import asyncio
from typing import Annotated

from fastapi import APIRouter, Query

from api.dependencies import DBSession, TokenData
from api.models.api_token import ApiTokenListRequest, ApiTokenListResponse
from common.models.user import UserRole
from common.sql.scripts.api_token import count_api_tokens
from common.sql.scripts.api_token import get_api_tokens as get_api_tokens_script

router = APIRouter()


@router.get("/", status_code=200, operation_id="Get Api Token List")
async def get_api_tokens(
    query: Annotated[ApiTokenListRequest, Query()],
    session_maker: DBSession,
    token_data: TokenData,
) -> ApiTokenListResponse:

    async with session_maker() as session:
        tokens, total = await asyncio.gather(
            get_api_tokens_script(
                session,
                customer_ids=query.customer_ids if token_data.is_(UserRole.ADMIN) else [token_data.id],
                limit=query.size,
                offset=query.offset,
            ),
            count_api_tokens(
                session,
                customer_ids=query.customer_ids if token_data.is_(UserRole.ADMIN) else [token_data.id],
            ),
        )

    return ApiTokenListResponse.new(
        tokens,
        total,
    )
