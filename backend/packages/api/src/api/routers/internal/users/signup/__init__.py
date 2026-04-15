from fastapi import APIRouter

from .new import router as new_router
from .validate import router as validate_router

router = APIRouter(prefix="/signup", tags=["signup"])

routers = [new_router, validate_router]

for r in routers:
    router.include_router(r)
