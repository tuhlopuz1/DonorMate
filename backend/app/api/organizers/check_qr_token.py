from typing import Annotated

from app.dependencies.checks import check_qr_data
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information
from app.models.schemas import ProfileResponse
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/check-qr", response_model=ProfileResponse)
async def check_qr_token(data: Annotated[dict, Depends(check_qr_data)]):
    if not data.get("user"):
        return badresponse("Invalid qr", 401)
    user = data["user"]
    user_info = await adapter.get_by_id(Information, user.id)
    return ProfileResponse.model_validate(user_info)
