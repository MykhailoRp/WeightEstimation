from datetime import datetime
from typing import Self

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.customer.api_token import ApiToken
from common.sql.tables.base import Base
from common.sql.tables.customer import CustomerTable
from common.types import UserId


class ApiTokenTable(Base):
    __tablename__ = "api_tokens"

    token: Mapped[str] = mapped_column(primary_key=True)
    customer_id: Mapped[UserId] = mapped_column(ForeignKey(CustomerTable.id))

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(True), server_default=func.now())

    # relationships
    customer: Mapped[CustomerTable] = relationship(back_populates="api_tokens")

    @classmethod
    def new(cls, m: ApiToken, /) -> Self:
        return cls(
            token=m.token,
            customer_id=m.customer_id,
            created_at=m.created_at,
        )

    def m(self) -> ApiToken:
        return ApiToken(
            token=self.token,
            customer_id=self.customer_id,
            created_at=self.created_at,
        )
