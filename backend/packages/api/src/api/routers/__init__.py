from fastapi import APIRouter

from api.routers.healthcheck import router as health_router

router = APIRouter()

routers = [health_router]

for r in routers:
    router.include_router(r)
