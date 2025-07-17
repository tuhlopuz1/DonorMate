from datetime import datetime, timezone
from typing import Annotated

from app.dependencies.checks import check_user_token
from app.dependencies.responses import badresponse
from app.models.db_adapter import adapter
from app.models.db_tables import Information, Registration
from app.models.schemas import ProfileResponse, Role
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/get-top-donors")
async def get_top_donors(user: Annotated[dict, Depends(check_user_token)]):
    if not user:
        return badresponse("Unauthorized", 401)
    if user.role != Role.ADMIN:
        return badresponse("Forbidden", 403)
    
    all_donors = await adapter.get_all(Registration)
    print(f"Total registrations: {len(all_donors)}")
    
    closed_donations = [reg for reg in all_donors if reg.closed]
    print(f"Closed donations: {len(closed_donations)}")
    
    if not closed_donations:
        return badresponse("No completed donations found", 404)
    
    donation_counts = {}
    for registration in closed_donations:
        user_id = registration.user_id
        print(f"Processing user_id: {user_id}")
        if user_id in donation_counts:
            donation_counts[user_id] += 1
        else:
            donation_counts[user_id] = 1
    
    print(f"Donation counts: {donation_counts}")
    
    top_donors = sorted(donation_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"Top donors: {top_donors}")

    result = []
    for user_id, donation_count in top_donors:
        print(f"Getting info for user_id: {user_id}")
        user_info = await adapter.get_by_id(Information, user_id)
        print(f"User info found: {user_info is not None}")
        if user_info:
            result.append({
                "user_id": user_id,
                "fullname": user_info.fullname,
                "surname": user_info.surname,
                "patronymic": user_info.patronymic,
                "donation_count": donation_count
            })
        else:
            result.append({
                "user_id": user_id,
                "fullname": "Unknown",
                "surname": "Unknown", 
                "patronymic": None,
                "donation_count": donation_count
            })
    
    print(f"Final result: {result}")
    return result
