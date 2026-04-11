from fastapi import APIRouter

from .login import router as login_router
from .logout import router as logout_router
from .me import router as me_router
from .refresh import router as refresh_router

router = APIRouter(prefix="/auth", tags=["auth"])

routers = [login_router, logout_router, me_router, refresh_router]

for r in routers:
    router.include_router(r)
