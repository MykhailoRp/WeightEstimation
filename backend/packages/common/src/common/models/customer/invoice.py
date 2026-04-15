import uuid
from datetime import UTC, datetime
from typing import Self

from pydantic import BaseModel

from common.models.ivoice import Currency, InvoiceStatus
from common.types import InvoiceId, UserId


class NewInvoice(BaseModel):
    id: InvoiceId
    customer_id: UserId

    amount: float
    currency: Currency

    created_at: datetime

    @classmethod
    def new(cls, customer_id: UserId, amount: float) -> Self:
        return cls(
            id=uuid.uuid4(),
            customer_id=customer_id,
            amount=amount,
            currency=Currency.UAH,
            created_at=datetime.now(tz=UTC),
        )


class Invoice(BaseModel):
    id: InvoiceId
    invoice_url: str
    customer_id: UserId

    amount: float
    currency: Currency

    created_at: datetime
    finished_at: datetime | None

    status: InvoiceStatus

    reason: str | None
    reason_code: str | None

    @classmethod
    def new(cls, m: NewInvoice, /, invoice_url: str) -> Self:
        return cls(
            id=m.id,
            invoice_url=invoice_url,
            customer_id=m.customer_id,
            created_at=NewInvoice.created_at,
            finished_at=None,
            amount=m.amount,
            currency=m.currency,
            status=InvoiceStatus.PROCESSING,
            reason=None,
            reason_code=None,
        )
