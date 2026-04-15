from fastapi import APIRouter

from .admin_id import router as admin_id_router
from .new import router as new_router

router = APIRouter(prefix="/admins", tags=["admin"])

routers = [new_router, admin_id_router]

for r in routers:
    router.include_router(r)
