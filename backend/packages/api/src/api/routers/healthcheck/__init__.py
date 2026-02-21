from fastapi import APIRouter

from api.routers.healthcheck.health import router as health_router

router = APIRouter(prefix="/health")

routers = [health_router]

for r in routers:
    router.include_router(r)
