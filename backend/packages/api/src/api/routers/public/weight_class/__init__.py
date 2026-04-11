from fastapi import APIRouter

from .list import router as list_router
from .new import router as new_router
from .weight_class_id import router as weight_class_id_router

router = APIRouter(prefix="/weight_classifications")

routers = [new_router, weight_class_id_router, list_router]

for r in routers:
    router.include_router(r)
