from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from app.models.schemas import ProfileResponse, Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-top-donors", response_model=list[ProfileResponse])
async def get_top_donors(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    donors = await adapter.get_all(Information)
    donors_dump = []
    for donor in donors:
        donor = ProfileResponse.model_validate(donor)
        donor.donations = donor.donations_fmba + donor.donations_gaur
    donors_dump.sort(key=lambda x: x.donations, reverse=True)
    donors_dump = donors_dump[:3]
    return donors_dump
