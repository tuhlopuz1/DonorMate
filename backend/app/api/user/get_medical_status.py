from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/get-medical-status")
async def get_med_status(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    return {"medical_exemption": user.info.medical_exemption}

