from fastapi import APIRouter, HTTPException, status

from api.auth.models import TokenData
from api.dependencies import DBSession, SecretsManager
from api.models.auth import RefreshRequest, RefreshResponse
from common.sql.scripts.user import get_user_with_role

router = APIRouter()


@router.post("/refresh", operation_id="Refresh Token")
async def refresh(
    request: RefreshRequest,
    secrets_manager: SecretsManager,
    session_maker: DBSession,
) -> RefreshResponse:
    async with session_maker() as session:
        user = await get_user_with_role(session, id=request.user_id, session_token=request.session)

        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown session")

    return RefreshResponse(access_token=secrets_manager.encode_token(user), data=TokenData.new(user))
