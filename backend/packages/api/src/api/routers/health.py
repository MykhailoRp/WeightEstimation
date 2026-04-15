import socket

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import OperationalError

from api.dependencies import DBSession
from api.models.basic import HealthCheck
from common.sql.scripts.ping import ping_db

router = APIRouter()


@router.get(path="/health")
async def health(session_maker: DBSession) -> HealthCheck:
    try:
        async with session_maker() as session:
            await ping_db(session=session)
    except (socket.gaierror, OperationalError) as e:
        raise HTTPException(status_code=503, detail="Service is unavalible") from e

    return HealthCheck(status=200, text="Service is healthy")
