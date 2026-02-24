from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

ALEMBIC_PATH = Path(__file__).parents[5].resolve() / "packages" / "db_setup" / "alembic.ini"


@pytest.fixture(scope="session")
def alembic_headed(created_database: None) -> None:
    command.upgrade(
        config=Config(
            file_=ALEMBIC_PATH,
        ),
        revision="head",
    )
