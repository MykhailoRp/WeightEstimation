from fastapi import APIRouter

from api.routers.users.user_id import router as user_id_router

router = APIRouter(prefix="/users")

routers = [user_id_router]

for r in routers:
    router.include_router(r)
