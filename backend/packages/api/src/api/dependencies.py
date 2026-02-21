from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from common.sql import DatabaseConfig

DATABASE_CONFIG = DatabaseConfig()


async def get_db_engine() -> AsyncEngine:
    return create_async_engine(DATABASE_CONFIG.url)


async def get_db_session(engine: Annotated[AsyncEngine, Depends(get_db_engine)]) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session


DatabaseSession = Annotated[AsyncSession, Depends(get_db_session)]
