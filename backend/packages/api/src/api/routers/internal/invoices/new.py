from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from api.dependencies import DBSession, InvoiceWrapper, TokenData
from api.models.invoice import InvoiceDetailsResponse, NewInvoiceRequest
from common.models.customer.invoice import NewInvoice
from common.models.user import UserRole
from common.sql.scripts.getters import get_user_with_role
from common.sql.tables.customer.invoice import InvoiceTable

router = APIRouter()


@router.post("/", status_code=200, operation_id="Create New Invoice")
async def new_invoice(
    request: Annotated[NewInvoiceRequest, Body()],
    session_maker: DBSession,
    invoice_wrapper: InvoiceWrapper,
    token_data: TokenData,
) -> InvoiceDetailsResponse:

    if request.customer_id != token_data.id and not token_data.is_(UserRole.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this customer")

    async with session_maker() as session:
        user = await get_user_with_role(session, id=request.customer_id)

        if user is None or not user.is_(UserRole.CUSTOMER):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cusomer does not exists")

        new_invoice = NewInvoice.new(customer_id=request.customer_id, amount=request.amount)

        final_invoice = await invoice_wrapper.request_invoice(user=user, invoice=new_invoice)

        session.add(InvoiceTable.new(final_invoice))
        await session.commit()

    return final_invoice
