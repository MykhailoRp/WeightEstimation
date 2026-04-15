from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from common.models.admin import Admin
from common.sql.tables import AdminTable
from common.types import UserId


async def get_admin(session: AsyncSession, *, id: UserId | None = None) -> Admin | None:
    statement = select(
        AdminTable,
    )

    if id is not None:
        statement = statement.where(AdminTable.id == id)

    result = (await session.execute(statement)).t.one_or_none()

    if result is None:
        return None

    (admin,) = result
    return admin.m()


async def is_subordinate(session: AsyncSession, *, requester_id: UserId, subordinate_id: UserId) -> bool:

    subordinates = select(AdminTable).where(AdminTable.id == requester_id).cte(name="subordinates", recursive=True)

    parent = aliased(AdminTable, name="p")

    subordinates = subordinates.union_all(select(parent).join(subordinates, onclause=subordinates.c.id == parent.promoted_by_id))

    final = exists(subordinates).select().where(subordinates.c.id == subordinate_id)

    response = await session.scalar(final)

    return response or False


async def demote_admin(session: AsyncSession, *, id: UserId) -> None:

    demotee_details = select(AdminTable).where(AdminTable.id == id)

    subordinates = aliased(AdminTable, name="s")

    update_subordinates = (
        update(subordinates).where(subordinates.promoted_by_id == demotee_details.c.id).values(promoted_by_id=demotee_details.c.promoted_by_id)
    )

    await session.execute(update_subordinates)
    await session.execute(delete(AdminTable).where(AdminTable.id == id))
