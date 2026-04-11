from fastapi import APIRouter

from api.routers.customers.customer_id.details import router as details_router

router = APIRouter(prefix="/{customer_id}")

routers = [details_router]

for r in routers:
    router.include_router(r)
