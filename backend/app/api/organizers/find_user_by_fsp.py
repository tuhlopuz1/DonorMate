from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from app.models.schemas import ProfileResponse, Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/find-user", response_model=list[ProfileResponse])
async def find_user(user: Annotated[User, Depends(check_user_token)], fsp: str):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    user_info = await adapter.find_similar_value(Information, "fsp", fsp)
    if not user_info:
        return badresponse("User not found", 404)
    users = []
    for user in user_info:
        user = ProfileResponse.model_validate(user)
        user.donations = sum(user.donations_fmba, user.donations_gaur)
        users.append(user)
    return users
