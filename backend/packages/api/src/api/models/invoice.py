from pydantic import BaseModel

from common.models.customer.invoice import Invoice
from common.types import UserId


class NewInvoiceRequest(BaseModel):
    customer_id: UserId
    amount: float


InvoiceDetailsResponse = Invoice
