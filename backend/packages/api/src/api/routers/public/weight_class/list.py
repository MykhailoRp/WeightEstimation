import asyncio
from typing import Annotated

from fastapi import APIRouter, Query

from api.dependencies import ApiUser, DBSession
from api.models.weight_class import WeightClassificationListRequest, WeightClassificationListResponse
from common.sql.scripts.getters import count_weight_classifications
from common.sql.scripts.getters import get_weight_classifications as get_weight_classifications_script

router = APIRouter()


@router.get("/", status_code=200, operation_id="Get Weight Classification List")
async def get_weight_classifications(
    query: Annotated[WeightClassificationListRequest, Query()],
    session_maker: DBSession,
    token_data: ApiUser,
) -> WeightClassificationListResponse:

    async with session_maker() as session:
        classifications, total = await asyncio.gather(
            get_weight_classifications_script(
                session,
                customer_ids=[token_data.customer_id],
                limit=query.size,
                offset=query.offset,
            ),
            count_weight_classifications(
                session,
                customer_ids=[token_data.customer_id],
            ),
        )

    return WeightClassificationListResponse.new(
        classifications,
        total,
    )
