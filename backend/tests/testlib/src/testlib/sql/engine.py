from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from common.sql.config import DatabaseConfig


@pytest.fixture(scope="session")
def db_engine(alembic_headed: None, db_config: DatabaseConfig) -> AsyncEngine:
    return create_async_engine(db_config.url)


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(db_engine) as session:
        yield session
