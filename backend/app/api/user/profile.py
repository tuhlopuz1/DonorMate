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

    response_data = {
        "user_id": user.id,
        "username": user.username,
        "tg_name": user.telegram_name,
        "role": user.role,
        "created_at": user.created_at,
    }

    if user_info:
        response_data.update(
            {
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
                "donations": user_info.donations,
            }
        )

    return ProfileResponse(**response_data)
