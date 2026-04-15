from fastapi import APIRouter

from .delete import router as delete_router

router = APIRouter(prefix="/{api_token}")

routers = [delete_router]

for r in routers:
    router.include_router(r)
