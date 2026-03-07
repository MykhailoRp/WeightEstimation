from fastapi import APIRouter

from api.routers.users.user_id.weight_class.new import router as new_router

router = APIRouter(prefix="/weight_classifications")

routers = [new_router]

for r in routers:
    router.include_router(r)
