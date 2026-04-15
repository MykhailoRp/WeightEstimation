from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from api.dependencies import DBSession, TokenData
from api.models.admin import AdminDetailsResponse
from common.models.user import UserRole
from common.sql.scripts.admin import get_admin as get_admin_script
from common.types import UserId

router = APIRouter()


@router.get("/", status_code=200, operation_id="Get Admin Details")
async def get_admin(
    admin_id: Annotated[UserId, Path()],
    session_maker: DBSession,
    token_data: TokenData,
) -> AdminDetailsResponse:

    if not token_data.is_(UserRole.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this admin")

    async with session_maker() as session:
        admin = await get_admin_script(session, id=admin_id)

    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    return AdminDetailsResponse.new(admin)
