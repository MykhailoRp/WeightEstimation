from fastapi import APIRouter

from api.routers.auth.login import router as login_router
from api.routers.auth.logout import router as logout_router
from api.routers.auth.me import router as me_router

router = APIRouter(prefix="/auth", tags=["auth"])

routers = [login_router, logout_router, me_router]

for r in routers:
    router.include_router(r)
