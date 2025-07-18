from datetime import datetime, timezone
from typing import Annotated

from app.dependencies.checks import check_qr_data
from app.dependencies.responses import badresponse, okresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, Registration
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/accept-donation")
async def accept_donation(data: Annotated[dict, Depends(check_qr_data)]):
    if not data.get("user"):
        return badresponse("Invalid qr", 401)
    user = data["user"]
    registration = data["registration"]
    user_info = await adapter.get_by_id(Information, user.id)
    await adapter.update_by_id(Registration, registration.id, {"closed": True, "closed_at": datetime.now(timezone.utc)})
    await adapter.update_by_id(Information, user.id, {"donations": user_info.donations + 1})
    return okresponse()
