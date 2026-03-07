from functools import lru_cache
from typing import Annotated

import aioboto3
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

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
def get_storage_session() -> aioboto3.Session:
    return aioboto3.Session(
        aws_access_key_id=STORAGE_CONFIG.access_key_id,
        aws_secret_access_key=STORAGE_CONFIG.secret_access_key,
    )


S3Session = Annotated[aioboto3.Session, Depends(get_storage_session)]
