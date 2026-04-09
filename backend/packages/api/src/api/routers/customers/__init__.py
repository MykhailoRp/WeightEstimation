from fastapi import APIRouter

from api.routers.customers.customer_id import router as customer_id_router

router = APIRouter(prefix="/customers", tags=["customer"])

routers = [customer_id_router]

for r in routers:
    router.include_router(r)
