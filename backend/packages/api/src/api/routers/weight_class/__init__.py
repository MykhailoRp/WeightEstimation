from fastapi import APIRouter

from api.routers.weight_class.new import router as new_router
from api.routers.weight_class.weight_class_id import router as weight_class_id_router

router = APIRouter(prefix="/weight_classifications", tags=["weight_classifications"])

routers = [new_router, weight_class_id_router]

for r in routers:
    router.include_router(r)
