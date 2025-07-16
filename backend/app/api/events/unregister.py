from typing import Annotated
from uuid import UUID

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse, emptyresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Event, Registration, User
from fastapi import APIRouter, Depends

router = APIRouter()


@router.delete("/register-on-event/{event_id}")
async def unregister_on_event(user: Annotated[User, Depends(check_user_token)], event_id: UUID):
    if not user:
        return badresponse("Unauthorized", 401)
    event = await adapter.get_by_id(Event, event_id)
    reg = await adapter.get_by_values(Registration, {"user_id": user.id, "event_id": event_id})
    if not reg:
        return badresponse("Registration not found", 404)
    reg = reg[0]
    await adapter.update_by_id(Event, event_id, {"registred", max(event.registred - 1, 0)})
    await adapter.delete(Registration, reg.id)
    return emptyresponse(204)
