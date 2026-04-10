from typing import Self

from pydantic import BaseModel

from common.models.customer import Customer
from common.types import UserId


class CustomerDetailsResponse(BaseModel):
    id: UserId
    funds: float

    @classmethod
    def new(cls, m: Customer) -> Self:
        return cls(
            id=m.id,
            funds=m.funds,
        )
