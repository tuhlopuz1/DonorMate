from typing import Annotated
from uuid import UUID

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Event, Registration, User
from app.models.schemas import EventSchema, Role, UserCreateSchema
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/create-user", response_model=UserCreateSchema)
async def create_user(user: Annotated[User, Depends(check_user_token)], created_user: UserCreateSchema):
    try:
        if not user:
            return badresponse("Unauthorized", 401)
        if user.role != Role.ADMIN:
            return badresponse("Forbidden", 403)
        created_user = created_user.model_dump()
        response = await adapter.insert(User, created_user)
        return response
    except Exception as e:
        return badresponse(str(e), 400)