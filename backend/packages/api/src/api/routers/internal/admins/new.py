from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from api.dependencies import DBSession, TokenData
from api.models.admin import AdminDetailsResponse, NewAdminRequest
from common.models.admin import Admin
from common.models.user import UserRole
from common.sql.tables.admin import AdminTable

router = APIRouter()


@router.post("/", status_code=200, operation_id="Create New Admin")
async def new_admin(
    request: Annotated[NewAdminRequest, Body()],
    session_maker: DBSession,
    token_data: TokenData,
) -> AdminDetailsResponse:

    if not token_data.is_(UserRole.ADMIN) or token_data.id == request.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can not create admins")

    admin = Admin(id=request.user_id, promoted_by_id=token_data.id)

    async with session_maker() as session:
        session.add(AdminTable.new(admin))
        await session.commit()

    return AdminDetailsResponse.new(admin)
