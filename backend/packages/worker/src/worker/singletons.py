from functools import lru_cache

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from common.s3 import S3Client, StorageConfig
from common.sql import DatabaseConfig

DATABASE_CONFIG = DatabaseConfig()

engine = create_async_engine(DATABASE_CONFIG.url)

session_maker = async_sessionmaker(engine, expire_on_commit=False)

STORAGE_CONFIG = StorageConfig()


@lru_cache(maxsize=1)
def client_maker() -> S3Client:
    return S3Client(config=STORAGE_CONFIG)
