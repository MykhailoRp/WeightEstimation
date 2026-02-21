from fastapi import APIRouter

from api.dependencies import DatabaseSession
from api.models.basic import HealthCheck
from common.sql.scripts.ping import ping_db

router = APIRouter()


@router.get(path="/")
async def health(session: DatabaseSession) -> HealthCheck:
    assert ping_db(session=session)
    return HealthCheck(status=200, text="Service api is healthy")
