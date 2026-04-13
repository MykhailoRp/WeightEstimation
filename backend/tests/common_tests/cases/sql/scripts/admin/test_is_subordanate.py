import uuid
from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.admin import Admin
from common.models.user import User
from common.sql.scripts.admin import is_subordinate
from common.sql.tables import UserTable
from common.sql.tables.admin import AdminTable
from common.types import UserId

user1 = User(
    id=UserId(uuid.UUID(int=1)),
    email="1",
    email_verified=True,
    password_hash="-",
    created_at=datetime.now(tz=UTC),
)

admin1 = Admin(
    id=user1.id,
    promoted_by_id=None,
)

user2 = User(
    id=UserId(uuid.UUID(int=2)),
    email="2",
    email_verified=True,
    password_hash="-",
    created_at=datetime.now(tz=UTC),
)

admin2 = Admin(
    id=user2.id,
    promoted_by_id=admin1.id,
)

user3 = User(
    id=UserId(uuid.UUID(int=3)),
    email="3",
    email_verified=True,
    password_hash="-",
    created_at=datetime.now(tz=UTC),
)

admin3 = Admin(
    id=user3.id,
    promoted_by_id=admin2.id,
)


@pytest_asyncio.fixture(scope="module")
async def module_session(session_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with session_session.begin_nested() as nested:
        session_session.add_all(
            [
                UserTable.new(user1),
                UserTable.new(user2),
                UserTable.new(user3),
                AdminTable.new(admin1),
                AdminTable.new(admin2),
                AdminTable.new(admin3),
            ],
        )
        await session_session.flush()
        yield session_session
        await nested.rollback()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "requester,subordinate,check",
    [
        (admin1.id, admin2.id, True),
        (admin1.id, admin3.id, True),
        (admin2.id, admin3.id, True),
        (admin3.id, admin1.id, False),
        (admin3.id, admin2.id, False),
        (admin2.id, admin1.id, False),
    ],
)
async def test_is_subordinate(function_session: AsyncSession, requester: UserId, subordinate: UserId, check: bool) -> None:  # noqa: FBT001
    assert await is_subordinate(function_session, requester_id=requester, subordinate_id=subordinate) == check
