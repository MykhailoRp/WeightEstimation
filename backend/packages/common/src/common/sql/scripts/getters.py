from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.user import UserWithRole
from common.sql.tables import AdminTable, CustomerTable, UserTable
from common.types import UserId


async def get_user_with_role(session: AsyncSession, *, id: UserId | None = None, email: str | None = None) -> UserWithRole | None:

    statement = (
        select(
            UserTable,
            AdminTable.id.isnot(None),
            CustomerTable.id.isnot(None),
        )
        .join(AdminTable, onclause=UserTable.id == AdminTable.id)
        .join(CustomerTable, onclause=UserTable.id == CustomerTable.id)
    )

    if id is not None:
        statement = statement.where(UserTable.id == id)

    if email is not None:
        statement = statement.where(UserTable.email == email)

    result = (await session.execute(statement)).one_or_none()

    if result is None:
        return None

    user, is_admin, is_customer = result

    return UserWithRole.new(user, is_admin=is_admin, is_customer=is_customer)
