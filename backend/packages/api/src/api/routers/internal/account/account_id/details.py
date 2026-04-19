from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from api.dependencies import DBSession, TokenData
from api.models.account import AccountDetailsResponse
from api.models.admin import AdminDetailsResponse
from api.models.customer import CustomerDetailsResponse
from api.models.user import UserDetailsResponse
from common.models.user import UserRole
from common.sql.scripts.admin import get_admin
from common.sql.scripts.getters import get_customer
from common.sql.scripts.user import get_user_with_role
from common.types import UserId

router = APIRouter()


@router.get("/", status_code=200, operation_id="Get Account Details")
async def get_user(
    account_id: Annotated[UserId, Path()],
    session_maker: DBSession,
    token_data: TokenData,
) -> AccountDetailsResponse:

    if account_id != token_data.id and not token_data.is_(UserRole.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this account")

    async with session_maker() as session:
        user = await get_user_with_role(session, id=account_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

        customer = await get_customer(session, id=account_id) if user.is_(UserRole.CUSTOMER) else None
        admin = await get_admin(session, id=account_id) if user.is_(UserRole.ADMIN) else None

    return AccountDetailsResponse(
        user=UserDetailsResponse.new(user),
        customer=CustomerDetailsResponse.new(customer) if customer else None,
        admin=AdminDetailsResponse.new(admin) if admin else None,
    )
