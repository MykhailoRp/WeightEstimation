from typing import Self

from pydantic import BaseModel

from api.models.basic import ListResponse, Paginated
from common.models.customer.api_token import ApiToken
from common.types import UserId


class NewApiTokenRequest(BaseModel):
    customer_id: UserId


ApiTokenDetailsResponse = ApiToken

ApiTokenItem = ApiToken


class ApiTokenListRequest(Paginated):
    customer_ids: list[UserId] | None = None


class ApiTokenListResponse(ListResponse[ApiTokenItem]):
    @classmethod
    def new(cls, m: list[ApiToken], total_count: int) -> Self:
        return cls(
            items=list(m),
            total_count=total_count,
        )
