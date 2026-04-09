from fastapi import APIRouter

from api.routers.customers.customer_id.weight_class import router as weight_class_router

router = APIRouter(prefix="/{customer_id}")

routers = [weight_class_router]

for r in routers:
    router.include_router(r)
