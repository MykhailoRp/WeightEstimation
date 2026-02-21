from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession


async def ping_db(session: AsyncSession) -> bool:
    return bool(await session.scalar(select(text("1"))))
