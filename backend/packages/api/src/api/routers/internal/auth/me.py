from fastapi import APIRouter

from api.dependencies import TokenData

router = APIRouter()


@router.get("/me", operation_id="Get Me")
async def me(
    token_data: TokenData,
) -> TokenData:
    return token_data
