from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import MedicalExemption, User
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-medical-exemptions")
async def get_me(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    me = await adapter.get_by_value(MedicalExemption, "user_id", user.id)
    if not me:
        return badresponse("Medical exemptions not found", 404)
    return me
