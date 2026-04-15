from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from common.sql.config import DatabaseConfig


@pytest.fixture(scope="session")
def db_engine(alembic_headed: None, db_config: DatabaseConfig) -> AsyncEngine:
    return create_async_engine(db_config.url)


@pytest_asyncio.fixture(scope="module")
async def session_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(db_engine) as session:
        temp_commit = session.commit
        session.commit = session.flush  # type: ignore[method-assign]
        temp_rollback = session.rollback
        session.rollback = AsyncMock()  # type: ignore[method-assign]
        async with session.begin_nested() as nested:
            yield session
            await nested.rollback()

        session.commit = temp_commit  # type: ignore[method-assign]
        session.rollback = temp_rollback  # type: ignore[method-assign]


@pytest_asyncio.fixture(scope="module")
async def module_session(session_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with session_session.begin_nested() as nested:
        yield session_session
        await nested.rollback()


@pytest_asyncio.fixture(scope="function")
async def function_session(module_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with module_session.begin_nested() as nested:
        yield module_session
        await nested.rollback()
