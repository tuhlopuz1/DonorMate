from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from app.models.schemas import DonorResponse, Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-top-donors")
async def get_top_donors(user: Annotated[dict, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    donors = await adapter.get_all_with_join(User, Information, "id")
    donors.sort(key=lambda donor: donor.donations)
    donors = donors[:3]
    result = []
    for donor in donors:
        result.append(DonorResponse.model_dump(donor))
    return result
