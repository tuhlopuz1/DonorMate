from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.csv_converter import CSVConverter
from app.models.db_adapter import adapter
from app.models.db_tables import Event, User
from app.models.schemas import EventResponse, Role
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/get-events-csv")
async def get_events_csv(user: Annotated[User, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    all_events = await adapter.get_all(Event)
    events_data = [EventResponse.model_dump(event) for event in all_events]
    csv_converter = CSVConverter()
    csv_file_path = await csv_converter.convert(events_data)
    return FileResponse(csv_file_path, media_type="text/csv", filename="events.csv", status_code=200)
