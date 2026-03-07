from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.dependencies import get_s3_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    s3_client = get_s3_client()
    await s3_client.safe_create_bucket()

    yield
