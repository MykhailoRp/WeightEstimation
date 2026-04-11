import secrets
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.auth import SecretsManager as _SecretsManager
from api.auth import SessionConfig, TokenConfig
from api.auth.conf import ApiTokenConfig
from api.auth.exc import InvalidTokenError, TokenExpiredError
from api.auth.models import ApiUser as _ApiUser
from api.auth.models import TokenData as _TokenData
from api.conf import ApiDocConfig
from api.payments import InvoiceWrapper as _InvoiceWrapper
from common.s3 import S3Client as _S3Client
from common.s3 import StorageConfig
from common.sql import DatabaseConfig
from common.sql.tables import ApiTokenTable

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
API_TOKEN_CONFIG = ApiTokenConfig()


@lru_cache(maxsize=1)
def get_secrets_manager() -> _SecretsManager:
    return _SecretsManager(token_conf=TOKEN_CONFIG, session_conf=SESSION_CONFIG, api_token_conf=API_TOKEN_CONFIG)


SecretsManager = Annotated[_SecretsManager, Depends(get_secrets_manager)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/internal/auth/login")


def get_token_data(token: Annotated[str, Depends(oauth2_scheme)], secrets_manager: SecretsManager) -> _TokenData:
    try:
        return secrets_manager.decode_token(token)
    except TokenExpiredError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers={"WWW-Authenticate": "Bearer"}) from e
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"}) from e


TokenData = Annotated[_TokenData, Depends(get_token_data)]


InvoiceWrapper = Annotated[_InvoiceWrapper, Depends()]


DOC_CONFIG = ApiDocConfig()


def docs_authenticate(credentials: HTTPBasicCredentials = Depends(HTTPBasic())) -> str:
    correct_username = secrets.compare_digest(credentials.username, DOC_CONFIG.username)
    correct_password = secrets.compare_digest(credentials.password, DOC_CONFIG.password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


api_token = APIKeyHeader(name="X-API-Key")


async def get_public_api_user(session_maker: DBSession, token: str = Security(api_token)) -> _ApiUser:

    async with session_maker() as session:
        customer_id = await session.scalar(select(ApiTokenTable.customer_id).where(ApiTokenTable.token == token))

    if customer_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )
    return _ApiUser(customer_id=customer_id)


ApiUser = Annotated[_ApiUser, Depends(get_public_api_user)]
