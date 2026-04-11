from fastapi import APIRouter

from .details import router as details_router
from .reset_email import router as reset_email_router

router = APIRouter(prefix="/{user_id}")

routers = [reset_email_router, details_router]

for r in routers:
    router.include_router(r)
