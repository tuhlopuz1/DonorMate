from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import User, Event
from app.models.schemas import Role, EventPayload

router = APIRouter()


@router.post("/create-event")
async def create_event(user: Annotated[User, Depends(check_user_token)], event: EventPayload):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    event_dict = EventPayload.model_dump(event)
    new_event = await adapter.insert(Event, event_dict)
    return okresponse(new_event.id)
