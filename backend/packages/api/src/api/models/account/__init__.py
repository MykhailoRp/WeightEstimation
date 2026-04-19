from pydantic import BaseModel

from api.models.admin import AdminDetailsResponse
from api.models.customer import CustomerDetailsResponse
from api.models.user import UserDetailsResponse


class AccountDetailsResponse(BaseModel):
    user: UserDetailsResponse
    admin: AdminDetailsResponse | None
    customer: CustomerDetailsResponse | None
