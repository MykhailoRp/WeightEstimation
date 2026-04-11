from typing import Any

from sqlalchemy import Select, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.customer.api_token import ApiToken
from common.sql.tables import ApiTokenTable
from common.types import ApiTokenStr, UserId


def apply_api_token_filter[T: Select[tuple[Any, ...]]](
    statement: T,
    *,
    token: ApiTokenStr | None,
    customer_ids: list[UserId] | None,
    limit: int | None,
    offset: int | None,
) -> T:
    if token is not None:
        statement = statement.where(ApiTokenTable.token == token)

    if customer_ids is not None:
        statement = statement.where(ApiTokenTable.customer_id.in_(customer_ids))

    if limit is not None:
        statement = statement.limit(limit)

    if offset is not None:
        statement = statement.offset(offset)

    return statement


async def count_api_tokens(
    session: AsyncSession,
    *,
    customer_ids: list[UserId] | None = None,
) -> int:
    statement = apply_api_token_filter(
        select(
            func.count(),
        ).select_from(ApiTokenTable),
        token=None,
        customer_ids=customer_ids,
        limit=None,
        offset=None,
    )

    result = await session.scalar(statement)

    return result or 0


async def get_api_tokens(
    session: AsyncSession,
    *,
    token: ApiTokenStr | None = None,
    customer_ids: list[UserId] | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[ApiToken]:
    statement = apply_api_token_filter(
        select(
            ApiTokenTable,
        ),
        token=token,
        customer_ids=customer_ids,
        limit=limit,
        offset=offset,
    )

    result = await session.scalars(statement)

    return [r.m() for r in result]


async def get_api_token(session: AsyncSession, *, token: ApiTokenStr | None, customer_id: UserId | None) -> ApiToken | None:
    results = await get_api_tokens(session, token=token, customer_ids=[customer_id] if customer_id else None, limit=1)

    return results[0] if len(results) == 1 else None


async def delete_token(session: AsyncSession, *, token: ApiTokenStr | None, customer_id: UserId | None) -> ApiToken | None:
    statement = delete(ApiTokenTable).returning(ApiTokenTable)

    if token is not None:
        statement = statement.where(ApiTokenTable.token == token)

    if customer_id is not None:
        statement = statement.where(ApiTokenTable.customer_id == customer_id)

    result = await session.scalar(statement)

    if result is None:
        return None

    return result.m()
