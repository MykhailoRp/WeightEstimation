from fastapi import APIRouter, HTTPException, status
from sqlalchemy import delete

from api.dependencies import DBSession, TokenData
from api.models.auth import LogoutRequest, LogoutResponse
from common.sql.tables.user.session import SessionTable

router = APIRouter()


@router.post("/logout", operation_id="Logout")
async def logout(
    request: LogoutRequest,
    token_data: TokenData,
    session_maker: DBSession,
) -> LogoutResponse:
    async with session_maker() as session:
        updated = await session.scalar(
            delete(SessionTable).where(SessionTable.user_id == token_data.id, SessionTable.token == request.session).returning(SessionTable.token),
        )

        if updated is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown session")

        await session.commit()

    return LogoutResponse()
