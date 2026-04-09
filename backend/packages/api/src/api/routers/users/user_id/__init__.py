from fastapi import APIRouter

from api.routers.users.user_id.reset_email import router as reset_email_router

router = APIRouter(prefix="/{user_id}")

routers = [reset_email_router]

for r in routers:
    router.include_router(r)
