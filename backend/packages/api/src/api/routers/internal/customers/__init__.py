from fastapi import APIRouter

from .customer_id import router as customer_id_router

router = APIRouter(prefix="/customers", tags=["customer"])

routers = [customer_id_router]

for r in routers:
    router.include_router(r)
