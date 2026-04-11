from fastapi import APIRouter

from .health import router as health_router
from .internal import router as internal_router
from .public import router as public_router
from .upload import router as upload_router

router = APIRouter(prefix="/api")

routers = [health_router, upload_router, internal_router, public_router]

for r in routers:
    router.include_router(r)
