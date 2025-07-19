from typing import Annotated
from uuid import UUID

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Event, Registration, User
from app.models.schemas import EventSchema, Role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/admin-get-event-by-id/{id}", response_model=EventSchema)
async def get_event_by_id(user: Annotated[User, Depends(check_user_token)], id: UUID):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    event = await adapter.get_by_id(Event, id)
    reg = await adapter.get_by_values(Registration, {"user_id": user.id, "event_id": event.id})
    event_dict = EventSchema.model_validate(event)
    if reg:
        event_dict.is_registred = True
    res = EventSchema.model_validate(event_dict).model_dump()
    donations = await adapter.get_by_value(Registration, "event_id", event.id)
    res["donations"] = len([i for i in donations if i.accepted])
    return res
