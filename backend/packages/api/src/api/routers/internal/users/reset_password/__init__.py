from fastapi import APIRouter

from .request import router as request_router
from .set import router as set_router

router = APIRouter(prefix="/reset_password")

routers = [request_router, set_router]

for r in routers:
    router.include_router(r)
