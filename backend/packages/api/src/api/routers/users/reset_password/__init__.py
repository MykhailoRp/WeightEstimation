from fastapi import APIRouter

from api.routers.users.reset_password.request import router as request_router
from api.routers.users.reset_password.set import router as set_router

router = APIRouter(prefix="/reset_password")

routers = [request_router, set_router]

for r in routers:
    router.include_router(r)
