from fastapi import APIRouter

from api.dependencies import TokenData

router = APIRouter()


@router.get("/me")
async def me(
    token_data: TokenData,
) -> TokenData:
    return token_data
