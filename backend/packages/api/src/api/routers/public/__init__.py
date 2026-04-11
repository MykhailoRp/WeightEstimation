from fastapi import APIRouter

from .upload import router as upload_router
from .weight_class import router as weight_class_router

router = APIRouter(prefix="/public", tags=["public"])

routers = [weight_class_router, upload_router]

for r in routers:
    router.include_router(r)
