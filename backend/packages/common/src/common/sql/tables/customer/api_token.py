from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.sql.tables.base import Base
from common.sql.tables.customer import CustomerTable
from common.types import UserId


class ApiTokenTable(Base):
    __tablename__ = "api_tokens"

    token: Mapped[str] = mapped_column(primary_key=True)
    customer_id: Mapped[UserId] = mapped_column(ForeignKey(CustomerTable.id))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # relationships
    customer: Mapped[CustomerTable] = relationship(back_populates="api_tokens")
