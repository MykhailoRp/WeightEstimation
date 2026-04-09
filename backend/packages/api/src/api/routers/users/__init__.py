from fastapi import APIRouter

from api.routers.users.signup import router as signup_router
from api.routers.users.user_id import router as user_id_router

router = APIRouter(prefix="/users", tags=["user"])

routers = [user_id_router, signup_router]

for r in routers:
    router.include_router(r)
