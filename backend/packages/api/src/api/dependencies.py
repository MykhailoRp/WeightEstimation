from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from common.sql import DatabaseConfig

DATABASE_CONFIG = DatabaseConfig()


engine = create_async_engine(DATABASE_CONFIG.url)


async def get_db_session() -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    yield async_sessionmaker(engine, expire_on_commit=False)


SessionMaker = Annotated[async_sessionmaker[AsyncSession], Depends(get_db_session)]
