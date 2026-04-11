from fastapi import APIRouter

from .reset_password import router as reset_password_router
from .signup import router as signup_router
from .user_id import router as user_id_router

router = APIRouter(prefix="/users", tags=["user"])

routers = [user_id_router, signup_router, reset_password_router]

for r in routers:
    router.include_router(r)
