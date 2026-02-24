import pytest
import pytest_asyncio
from sqlalchemy_utils import create_database, database_exists

from common.sql import DatabaseConfig


@pytest.fixture(scope="session")
def db_config() -> DatabaseConfig:
    return DatabaseConfig()


@pytest_asyncio.fixture(scope="session")
async def created_database(db_config: DatabaseConfig) -> None:
    if not database_exists(db_config.url):
        create_database(db_config.url)
