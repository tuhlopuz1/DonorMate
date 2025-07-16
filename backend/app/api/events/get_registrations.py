from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Registration, User
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-registrations")
async def get_user_reg(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    registrations = await adapter.get_by_value(Registration, "user_id", user.id)
    if not registrations:
        return badresponse("Registrations not found", 404)
    return registrations
