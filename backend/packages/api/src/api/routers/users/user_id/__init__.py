from fastapi import APIRouter

from api.routers.users.user_id.weight_class import router as weight_class_router

router = APIRouter(prefix="/{user_id}")

routers = [weight_class_router]

for r in routers:
    router.include_router(r)
