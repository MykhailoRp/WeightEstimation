from typing import Self

from pydantic import BaseModel

from api.models.basic import ListResponse, Paginated
from common.models.customer.invoice import Invoice
from common.types import UserId


class NewInvoiceRequest(BaseModel):
    customer_id: UserId
    amount: float


InvoiceDetailsResponse = Invoice


class InvoiceListRequest(Paginated):
    customer_ids: list[UserId] | None = None


InvoiceListItem = Invoice


class InvoiceListResponse(ListResponse[InvoiceListItem]):
    @classmethod
    def new(cls, m: list[Invoice], total_count: int) -> Self:
        return cls(
            items=list(m),
            total_count=total_count,
        )
