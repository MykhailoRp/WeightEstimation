from fastapi import APIRouter

from .invoice_id import router as invoice_id_router
from .list import router as list_router
from .new import router as new_router

router = APIRouter(prefix="/invoices", tags=["invoices"])

routers = [list_router, new_router, invoice_id_router]

for r in routers:
    router.include_router(r)
