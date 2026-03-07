from fastapi import APIRouter

from api.routers.health import router as health_router
from api.routers.upload import router as upload_router

router = APIRouter()

routers = [health_router, upload_router]

for r in routers:
    router.include_router(r)
