from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from app.models.schemas import ProfileResponse
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)

    user_info = await adapter.get_by_id(Information, user.id)
    response_data = ProfileResponse.model_validate(user_info)
    response_data.donations = sum(response_data.donations_fmba, response_data.donations_gaur)
    return response_data
