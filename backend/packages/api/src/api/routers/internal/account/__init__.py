from fastapi import APIRouter

from .account_id import router as account_id_router

router = APIRouter(prefix="/account")

routers = [account_id_router]

for r in routers:
    router.include_router(r)
