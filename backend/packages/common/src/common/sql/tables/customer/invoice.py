from datetime import datetime
from typing import Self

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.customer.invoice import Invoice
from common.models.ivoice import Currency, InvoiceStatus
from common.sql.tables.base import Base
from common.sql.tables.customer import CustomerTable
from common.types import InvoiceId, UserId


class InvoiceTable(Base):
    __tablename__ = "invoices"

    id: Mapped[InvoiceId] = mapped_column(primary_key=True)
    invoice_url: Mapped[str] = mapped_column(unique=True)
    customer_id: Mapped[UserId] = mapped_column(ForeignKey(CustomerTable.id))

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(True))

    amount: Mapped[float]
    currency: Mapped[Currency]

    status: Mapped[InvoiceStatus]

    reason: Mapped[str | None]
    reason_code: Mapped[str | None]

    # relationships
    customer: Mapped[CustomerTable] = relationship(back_populates="invoices")

    @classmethod
    def new(cls, m: Invoice) -> Self:
        return cls(
            id=m.id,
            invoice_url=m.invoice_url,
            customer_id=m.customer_id,
            created_at=m.created_at,
            finished_at=m.finished_at,
            amount=m.amount,
            currency=m.currency,
            status=m.status,
            reason=m.reason,
            reason_code=m.reason_code,
        )

    def m(self) -> Invoice:
        return Invoice(
            id=self.id,
            invoice_url=self.invoice_url,
            customer_id=self.customer_id,
            created_at=self.created_at,
            finished_at=self.finished_at,
            amount=self.amount,
            currency=self.currency,
            status=self.status,
            reason=self.reason,
            reason_code=self.reason_code,
        )
