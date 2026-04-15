from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from api.dependencies import DBSession, TokenData
from api.models.customer import CustomerDetailsResponse
from common.models.user import UserRole
from common.sql.scripts.getters import get_customer as get_customer_script
from common.types import UserId

router = APIRouter()


@router.get("/", status_code=200, operation_id="Get Customer Details")
async def get_customer(
    customer_id: Annotated[UserId, Path()],
    session_maker: DBSession,
    token_data: TokenData,
) -> CustomerDetailsResponse:

    if customer_id != token_data.id and not token_data.is_(UserRole.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this customer")

    async with session_maker() as session:
        customer = await get_customer_script(session, id=customer_id)

    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    return CustomerDetailsResponse.new(customer)
