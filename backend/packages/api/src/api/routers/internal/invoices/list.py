from typing import Annotated

from fastapi import APIRouter, Query

from api.dependencies import DBSession, TokenData
from api.models.invoice import InvoiceListRequest, InvoiceListResponse
from common.models.user import UserRole
from common.sql.scripts.invoice import count_invoices
from common.sql.scripts.invoice import get_invoices as get_invoices_script

router = APIRouter()


@router.get("/", status_code=200, operation_id="Get Invoices List")
async def get_invoices(
    query: Annotated[InvoiceListRequest, Query()],
    session_maker: DBSession,
    token_data: TokenData,
) -> InvoiceListResponse:

    async with session_maker() as session:
        classifications = await get_invoices_script(
            session,
            customer_ids=query.customer_ids if token_data.is_(UserRole.ADMIN) else [token_data.id],
            limit=query.size,
            offset=query.offset,
        )
        total = await count_invoices(
            session,
            customer_ids=query.customer_ids if token_data.is_(UserRole.ADMIN) else [token_data.id],
        )

    return InvoiceListResponse.new(
        classifications,
        total,
    )
