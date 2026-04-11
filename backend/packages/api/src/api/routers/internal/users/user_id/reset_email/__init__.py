from fastapi import APIRouter

from .request import router as request_router
from .validate import router as validate_router

router = APIRouter(prefix="/reset_email")

routers = [request_router, validate_router]

for r in routers:
    router.include_router(r)
