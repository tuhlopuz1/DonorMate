from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Event, Registration, User
from app.models.schemas import EventSchema
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-all-events", response_model=list[EventSchema])
async def get_all_events(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    events = await adapter.get_all(Event)
    if not events:
        return badresponse("No events found", 404)
    events_sch = []
    for event in events:
        event = EventSchema.model_validate(event)
        reg = await adapter.get_by_values(Registration, {"user_id": user.id, "event_id": event.id})
        if reg:
            event.is_registred = True
        events_sch.append(event)
    return events_sch
