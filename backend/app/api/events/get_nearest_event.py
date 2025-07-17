from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Event, User
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/get-nearest-event")
async def get_all_events(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    events = await adapter.get_all(Event)
    if not events:
        return badresponse("No events found", 404)
    events.sort(key=lambda x: x.start_date)
    return events