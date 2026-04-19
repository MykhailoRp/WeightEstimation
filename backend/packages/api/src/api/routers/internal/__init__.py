from fastapi import APIRouter

from .account import router as account_router
from .admins import router as admins_router
from .api_tokens import router as api_tokens_router
from .auth import router as auth_router
from .customers import router as customers_router
from .invoices import router as invoices_router
from .upload import router as upload_router
from .users import router as users_router
from .weight_class import router as weight_class_router

router = APIRouter(prefix="/internal")

routers = [users_router, auth_router, customers_router, weight_class_router, invoices_router, api_tokens_router, upload_router, admins_router, account_router]

for r in routers:
    router.include_router(r)
