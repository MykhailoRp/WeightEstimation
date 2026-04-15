from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from api.dependencies import DBSession, TokenData
from api.models.invoice import InvoiceDetailsResponse
from common.models.user import UserRole
from common.sql.scripts.invoice import get_invoice as get_invoice_script
from common.types import InvoiceId

router = APIRouter()


@router.get("/", status_code=200, operation_id="Get Invoice Details")
async def get_invoice(
    invoice_id: Annotated[InvoiceId, Path()],
    session_maker: DBSession,
    token_data: TokenData,
) -> InvoiceDetailsResponse:

    async with session_maker() as session:
        result = await get_invoice_script(
            session,
            id=invoice_id,
            customer_id=None if token_data.is_(UserRole.ADMIN) else token_data.id,
        )

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")

    return result
