from collections.abc import Iterable
from typing import Any, Final

from sqlalchemy import ColumnElement, ColumnExpressionArgument, Select, case, func, select
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.user import UserRole, UserWithRole, new_user_with_role
from common.sql.tables import AdminTable, CustomerTable, SessionTable, UserTable
from common.types import UserId

USER_ROLES: Final[ColumnElement[list[UserRole]]] = func.array_remove(
    array(
        [
            case((select(AdminTable.id).where(AdminTable.id == UserTable.id).exists(), UserRole.ADMIN), else_=None),
            case((select(CustomerTable.id).where(CustomerTable.id == UserTable.id).exists(), UserRole.CUSTOMER), else_=None),
        ],
    ),
    None,
)


def apply_pagination[T: tuple[Any, ...]](
    statement: Select[T],
    *,
    limit: int | None,
    offset: int | None,
    order_by: ColumnExpressionArgument | None,
) -> Select[T]:

    if limit is not None:
        statement = statement.limit(limit)

    if offset is not None:
        statement = statement.offset(offset)

    if order_by is not None:
        statement = statement.order_by(order_by)

    return statement


def apply_user_filter[T: tuple[Any, ...]](
    statement: Select[T],
    *,
    id: UserId | None,
    email: str | None,
    email_like: str | None,
    session_token: str | None,
    roles: Iterable[UserRole] | None,
) -> Select[T]:

    if id is not None:
        statement = statement.where(UserTable.id == id)

    if email is not None:
        statement = statement.where(UserTable.email == email)

    if email_like is not None:
        statement = statement.where(UserTable.email.ilike(f"%{email_like}%"))

    if session_token is not None:
        statement = statement.join(SessionTable).where(SessionTable.token == session_token, SessionTable.expire_at > func.now())

    if roles is not None:
        statement = statement.where(USER_ROLES.op("&&")(roles))

    return statement


async def count_users(
    session: AsyncSession,
    *,
    email_like: str | None,
    roles: set[UserRole] | None,
) -> int:
    statement = apply_user_filter(
        select(
            func.count(),
        ).select_from(UserTable),
        email_like=email_like,
        roles=roles,
        id=None,
        email=None,
        session_token=None,
    )

    result = await session.scalar(statement)

    return result or 0


async def get_users(
    session: AsyncSession,
    *,
    id: UserId | None = None,
    email: str | None = None,
    email_like: str | None = None,
    session_token: str | None = None,
    roles: Iterable[UserRole] | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[UserWithRole]:
    statement = apply_user_filter(
        select(
            UserTable,
            USER_ROLES,
        ),
        email_like=email_like,
        roles=roles,
        id=id,
        email=email,
        session_token=session_token,
    )

    statement = apply_pagination(
        statement,
        limit=limit,
        offset=offset,
        order_by=None,
    )

    result = await session.execute(statement)

    return [new_user_with_role(user.m(), roles=roles) for user, roles in result.t.all()]


async def get_user_with_role(
    session: AsyncSession,
    *,
    id: UserId | None = None,
    email: str | None = None,
    session_token: str | None = None,
) -> UserWithRole | None:
    results = await get_users(session, id=id, email=email, session_token=session_token, limit=1)

    return results[0] if len(results) == 1 else None
