from fastapi import APIRouter

from .delete import router as delete_router
from .details import router as details_router

router = APIRouter(prefix="/{admin_id}")

routers = [details_router, delete_router]

for r in routers:
    router.include_router(r)
