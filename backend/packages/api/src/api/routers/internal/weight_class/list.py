from typing import Annotated

from fastapi import APIRouter, Query

from api.dependencies import DBSession, TokenData
from api.models.weight_class import WeightClassificationListRequest, WeightClassificationListResponse
from common.models.user import UserRole
from common.sql.scripts.getters import count_weight_classifications
from common.sql.scripts.getters import get_weight_classifications as get_weight_classifications_script

router = APIRouter()


@router.get("/", status_code=200, operation_id="Get Weight Classification List")
async def get_weight_classifications(
    query: Annotated[WeightClassificationListRequest, Query()],
    session_maker: DBSession,
    token_data: TokenData,
) -> WeightClassificationListResponse:

    async with session_maker() as session:
        classifications = await get_weight_classifications_script(
            session,
            customer_ids=query.customer_ids if token_data.is_(UserRole.ADMIN) else [token_data.id],
            limit=query.size,
            offset=query.offset,
        )
        total = await count_weight_classifications(
            session,
            customer_ids=query.customer_ids if token_data.is_(UserRole.ADMIN) else [token_data.id],
        )

    return WeightClassificationListResponse.new(
        classifications,
        total,
    )
