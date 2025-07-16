from datetime import datetime, timezone
from typing import Annotated

from app.dependencies.checks import check_qr_data
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, Registration
from app.models.schemas import ProfileResponse
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/check-qr", response_model=ProfileResponse)
async def check_qr_token(data: Annotated[dict, Depends(check_qr_data)]):
    if not data.get("user"):
        return badresponse("Invalid qr", 401)
    user = data["user"]
    registration = data["registration"]
    user_info = await adapter.get_by_id(Information, user.id)
    response_data = {
        "user_id": user.id,
        "username": user.username,
        "tg_name": user.telegram_name,
        "role": user.role,
        "created_at": user.created_at,
        "fullname": user_info.fullname,
        "surname": user_info.surname,
        "patronymic": user_info.patronymic,
        "birth_date": user_info.birth_date,
        "gender": user_info.gender,
        "university": user_info.university,
        "group": user_info.group,
        "weight": user_info.weight,
        "chronic_disease": user_info.chronic_disease,
        "medical_exemption": user_info.medical_exemption,
        "donor_earlier": user_info.donor_earlier,
    }
    await adapter.update_by_id(Registration, registration.id, {"closed": True, "closed_at": datetime.now(timezone.utc)})
    return ProfileResponse(**response_data)
