from typing import Annotated
from uuid import UUID

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Event, Registration, User
from app.models.schemas import EventSchema
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-event-by-id/{id}", response_model=EventSchema)
async def get_event_by_id(user: Annotated[User, Depends(check_user_token)], id: UUID):
    if not user:
        return badresponse("Unauthorized", 401)
    event = await adapter.get_by_id(Event, id)
    reg = await adapter.get_by_values(Registration, {"user_id": user.id, "event_id": event.id})
    event_dict = EventSchema.model_validate(event)
    if reg:
        event_dict.is_registred = True
    return EventSchema.model_validate(event_dict)
