#!/usr/bin/env python

import asyncio
import uuid
from datetime import UTC, datetime

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from api.auth import ApiTokenConfig, SecretsManager, SessionConfig, TokenConfig
from common.models.admin import Admin
from common.models.user import User
from common.sql.config import DatabaseConfig
from common.sql.tables.admin import AdminTable
from common.sql.tables.user import UserTable

secret = SecretsManager(TokenConfig(), SessionConfig(), ApiTokenConfig())


users = [
    User(
        id=uuid.UUID(int=1),
        email="tempmail1@mail.com",
        email_verified=True,
        password_hash=secret.hash_pass("Password1$"),
        created_at=datetime.now(tz=UTC),
    ),
    User(
        id=uuid.UUID(int=2),
        email="tempmail2@mail.com",
        email_verified=True,
        password_hash=secret.hash_pass("Password1$"),
        created_at=datetime.now(tz=UTC),
    ),
]

admins = [
    Admin(
        id=users[0].id,
        promoted_by_id=None,
    ),
]


async def main() -> None:
    database_engine = create_async_engine(DatabaseConfig().url)

    async with AsyncSession(database_engine) as session:
        logger.info("Users")
        for user in users:
            session.add(UserTable.new(user))

        logger.info("Admins")
        for admin in admins:
            session.add(AdminTable.new(admin))

        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
