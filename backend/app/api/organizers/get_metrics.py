from datetime import datetime, timezone
from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Event, Information, User
from app.models.schemas import MetricsResponse, Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-metrics", response_model=MetricsResponse)
async def metrics(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    users = await adapter.get_all_with_join(User, Information, "phone", False)
    users_count = len(users) if users else 0
    donations_fmba_count = await adapter.get_column_sum(Information, "donations_fmba_count") if users else 0
    donations_gaur_count = await adapter.get_column_sum(Information, "donations_gaur_count") if users else 0
    donations_count = donations_fmba_count + donations_gaur_count
    new_events_count = (
        await adapter.get_count_cond(Event, "start_date", datetime.now(timezone.utc), ">") if users else 0
    )
    ended_events_count = (
        await adapter.get_count_cond(Event, "end_date", datetime.now(timezone.utc), "<") if users else 0
    )
    return MetricsResponse(
        users_count=users_count,
        donations_fmba_count=donations_fmba_count,
        donations_gaur_count=donations_gaur_count,
        donations_count=donations_count,
        new_events_count=new_events_count,
        ended_events_count=ended_events_count,
    )
