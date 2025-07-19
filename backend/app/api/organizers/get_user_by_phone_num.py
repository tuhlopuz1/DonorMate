from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from app.models.schemas import ProfileResponse, Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-user/{num}", response_model=ProfileResponse)
async def get_user(user: Annotated[User, Depends(check_user_token)], num: int):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    user_info = await adapter.get_by_value(Information, "phone", num)
    if not user_info:
        return badresponse("User not found", 404)
    response = ProfileResponse.model_validate(user_info)
    response.donations = response.donations_fmba + response.donations_gaur
    return response
