from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.ivoice import Currency, InvoiceStatus
from common.sql.tables.base import Base
from common.sql.tables.customer import CustomerTable
from common.types import InvoiceId, UserId


class InvoiceTable(Base):
    __tablename__ = "invoices"

    id: Mapped[InvoiceId] = mapped_column(primary_key=True)
    customer_id: Mapped[UserId] = mapped_column(ForeignKey(CustomerTable.id))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    finished_at: Mapped[datetime | None]

    amount: Mapped[float]
    currency: Mapped[Currency]

    status: Mapped[InvoiceStatus]

    reason: Mapped[str | None]
    reason_code: Mapped[str | None]

    # relationships
    customer: Mapped[CustomerTable] = relationship(back_populates="invoices")
