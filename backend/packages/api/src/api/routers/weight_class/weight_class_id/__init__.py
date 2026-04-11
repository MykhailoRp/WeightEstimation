from fastapi import APIRouter

from api.routers.weight_class.weight_class_id.details import router as details_router

router = APIRouter(prefix="/{weight_class_id}")

routers = [details_router]

for r in routers:
    router.include_router(r)
