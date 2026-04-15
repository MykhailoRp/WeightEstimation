from typing import Self

from pydantic import BaseModel

from common.types import UserId


class Customer(BaseModel):
    id: UserId
    funds: float

    @classmethod
    def new(cls, user_id: UserId) -> Self:
        return cls(
            id=user_id,
            funds=0.0,
        )
