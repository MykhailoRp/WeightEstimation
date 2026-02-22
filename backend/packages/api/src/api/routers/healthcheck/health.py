import socket

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import OperationalError

from api.dependencies import DatabaseSession
from api.models.basic import HealthCheck
from common.sql.scripts.ping import ping_db

router = APIRouter()


@router.get(path="/")
async def health(session: DatabaseSession) -> HealthCheck:
    try:
        await ping_db(session=session)
    except (socket.gaierror, OperationalError) as e:
        raise HTTPException(status_code=503, detail="Service unavalible") from e

    return HealthCheck(status=200, text="Service api is healthy")
