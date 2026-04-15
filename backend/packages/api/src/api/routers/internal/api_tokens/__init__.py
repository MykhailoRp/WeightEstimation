from fastapi import APIRouter

from .api_token import router as api_token_router
from .list import router as list_router
from .new import router as new_router

router = APIRouter(prefix="/api_tokens", tags=["api_tokens"])

routers = [new_router, list_router, api_token_router]

for r in routers:
    router.include_router(r)
