from typing import Annotated

from datetime import datetime, timedelta
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Event, User, Registration
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/get-notifications-for-users")
async def get_notifications_for_users():
    events = await adapter.get_all(Event)
    events.sort(key=lambda x: x.start_date, reverse=True)
    close_events = []
    for i in events:
        if i.start_date > datetime.now() - timedelta(days=1):
            close_events.append(str(i.id))
    res = []
    for i in close_events:
        user_ids = await adapter.get_by_value(Registration, "event_id", i)
        for j in user_ids:
            res.append(j.user_id)
    res = list(set(res))
    res.sort()
    return res


    