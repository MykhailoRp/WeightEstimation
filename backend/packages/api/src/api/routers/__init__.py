from fastapi import APIRouter

from api.routers.auth import router as auth_router
from api.routers.health import router as health_router
from api.routers.upload import router as upload_router
from api.routers.users import router as users_router

router = APIRouter()

routers = [health_router, upload_router, users_router, auth_router]

for r in routers:
    router.include_router(r)
