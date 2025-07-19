from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from app.models.schemas import ProfileResponse, Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/create-user", response_model=ProfileResponse)
async def create_user(user: Annotated[User, Depends(check_user_token)], created_user: ProfileResponse):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    created_user = ProfileResponse.model_dump(created_user)
    response = await adapter.insert(Information, created_user)
    return ProfileResponse.model_validate(response)
