from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from common.s3 import S3Client as _S3Client
from common.s3 import StorageCongfig
from common.sql import DatabaseConfig

DATABASE_CONFIG = DatabaseConfig()

database_engine = create_async_engine(DATABASE_CONFIG.url)


@lru_cache(maxsize=1)
def get_db_session() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(database_engine, expire_on_commit=False)


DBSession = Annotated[async_sessionmaker[AsyncSession], Depends(get_db_session)]


STORAGE_CONFIG = StorageCongfig()


@lru_cache(maxsize=1)
def get_s3_client() -> _S3Client:
    return _S3Client(config=STORAGE_CONFIG)


S3Client = Annotated[_S3Client, Depends(get_s3_client)]
