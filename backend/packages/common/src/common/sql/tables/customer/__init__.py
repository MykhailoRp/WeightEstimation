from typing import TYPE_CHECKING, Self

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.customer import Customer
from common.sql.tables.base import Base
from common.sql.tables.user import UserTable
from common.types import UserId

if TYPE_CHECKING:
    from common.sql.tables.customer.api_token import ApiTokenTable
    from common.sql.tables.customer.invoice import InvoiceTable
    from common.sql.tables.customer.weight_class import WeightClassificationTable


class CustomerTable(Base):
    __tablename__ = "customers"

    id: Mapped[UserId] = mapped_column(ForeignKey(UserTable.id), primary_key=True)
    funds: Mapped[float]

    # relationships
    user: Mapped[UserTable] = relationship(back_populates="customer")
    invoices: Mapped[list["InvoiceTable"]] = relationship(back_populates="customer")
    api_tokens: Mapped[list["ApiTokenTable"]] = relationship(back_populates="customer")
    weight_classifications: Mapped[list["WeightClassificationTable"]] = relationship(back_populates="customer")

    @classmethod
    def new(cls, m: Customer, /) -> Self:
        return cls(
            id=m.id,
            funds=m.funds,
        )

    def m(self) -> Customer:
        return Customer(
            id=self.id,
            funds=self.funds,
        )
