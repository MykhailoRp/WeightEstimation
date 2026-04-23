from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from api.dependencies import DBSession, TokenData
from api.models.admin import DemoteAdminResponse
from common.models.user import UserRole
from common.sql.scripts.admin import demote_admin as demote_admin_script
from common.sql.scripts.admin import is_subordinate
from common.types import UserId

router = APIRouter()


@router.delete("/", status_code=200, operation_id="Demote Admin")
async def delete_admin(
    admin_id: Annotated[UserId, Path()],
    session_maker: DBSession,
    token_data: TokenData,
) -> DemoteAdminResponse:

    if not token_data.is_(UserRole.ADMIN) or token_data.id == admin_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this admin")

    async with session_maker() as session:
        if not await is_subordinate(session, requester_id=token_data.id, subordinate_id=admin_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cant demote this admin")

        await demote_admin_script(session, id=admin_id)
        await session.commit()

    return DemoteAdminResponse()
