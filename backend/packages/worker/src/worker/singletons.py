from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from common.sql import DatabaseConfig

DATABASE_CONFIG = DatabaseConfig()

engine = create_async_engine(DATABASE_CONFIG.url)

session_maker = async_sessionmaker(engine, expire_on_commit=False)
