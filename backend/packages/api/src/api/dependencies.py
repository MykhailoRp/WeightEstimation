from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.auth import SecretsManager as _SecretsManager
from api.auth import SessionConfig, TokenConfig
from api.auth.exc import InvalidTokenError, TokenExpiredError
from api.auth.models import TokenData as _TokenData
from common.s3 import S3Client as _S3Client
from common.s3 import StorageConfig
from common.sql import DatabaseConfig

DATABASE_CONFIG = DatabaseConfig()

database_engine = create_async_engine(DATABASE_CONFIG.url)


@lru_cache(maxsize=1)
def get_db_session() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(database_engine, expire_on_commit=False)


DBSession = Annotated[async_sessionmaker[AsyncSession], Depends(get_db_session)]


STORAGE_CONFIG = StorageConfig()


@lru_cache(maxsize=1)
def get_s3_client() -> _S3Client:
    return _S3Client(config=STORAGE_CONFIG)


S3Client = Annotated[_S3Client, Depends(get_s3_client)]


TOKEN_CONFIG = TokenConfig()
SESSION_CONFIG = SessionConfig()


@lru_cache(maxsize=1)
def get_secrets_manager() -> _SecretsManager:
    return _SecretsManager(token_conf=TOKEN_CONFIG, session_conf=SESSION_CONFIG)


SecretsManager = Annotated[_SecretsManager, Depends(get_secrets_manager)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_token_data(token: Annotated[str, Depends(oauth2_scheme)], secrets_manager: SecretsManager) -> _TokenData:
    try:
        return secrets_manager.decode_token(token)
    except TokenExpiredError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired", headers={"WWW-Authenticate": "Bearer"}) from e
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"}) from e


TokenData = Annotated[_TokenData, Depends(get_token_data)]
