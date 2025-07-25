from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, User
from app.models.schemas import Role, RoleMetricsResponse
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-role-metrics", response_model=RoleMetricsResponse)
async def get_role_metrics(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    users_count = await adapter.get_count_cond(User, "role", Role.ADMIN, "!=")
    admins_count = await adapter.get_count_cond(User, "role", Role.ADMIN, "==")
    donors_count_fmba = await adapter.get_count_cond(Information, "donations_fmba", 1, ">=")
    const_donors_count_fmba = await adapter.get_count_cond(Information, "donations_fmba", 3, ">=")
    donors_count_gaur = await adapter.get_count_cond(Information, "donations_gaur", 1, ">=")
    const_donors_count_gaur = await adapter.get_count_cond(Information, "donations_gaur", 3, ">=")
    donors_count = donors_count_fmba + donors_count_gaur
    const_donors_count = const_donors_count_fmba + const_donors_count_gaur
    return RoleMetricsResponse(
        users_count=users_count,
        admins_count=admins_count,
        donors_count_fmba=donors_count_fmba,
        const_donors_count_fmba=const_donors_count_fmba,
        donors_count_gaur=donors_count_gaur,
        const_donors_count_gaur=const_donors_count_gaur,
        donors_count=donors_count,
        const_donors_count=const_donors_count,
    )
