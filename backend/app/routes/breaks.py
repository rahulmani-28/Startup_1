from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from ..core.db import get_database
from ..models.schemas import (
    BreakSuggestionRequest,
    BreakSuggestion,
    BreakRecordRequest,
    BreakRecordResponse,
)

router = APIRouter(prefix="/breaks", tags=["breaks"])

@router.post("/suggest", response_model=BreakSuggestion)
async def suggest_break(
    payload: BreakSuggestionRequest, db: AsyncIOMotorDatabase = Depends(get_database)
) -> BreakSuggestion:
    # Logic: Suggest break if driven > 200km OR > 3 hours
    # In a real app, we'd check the journey history.
    # Here we rely on client payload for simplicity.
    
    should_break = False
    reason = None
    
    if payload.total_distance_km > 200:
        should_break = True
        reason = "You have driven over 200km."
    elif payload.elapsed_time_hours > 3:
        should_break = True
        reason = "You have been driving for over 3 hours."
        
    return BreakSuggestion(should_take_break=should_break, reason=reason, nearby_hotels_count=5)


@router.post("/record", response_model=BreakRecordResponse)
async def record_break(
    payload: BreakRecordRequest, db: AsyncIOMotorDatabase = Depends(get_database)
) -> BreakRecordResponse:
    breaks = db.get_collection("Breaks")
    doc = {
        "journey_id": payload.journey_id,
        "location": payload.location.model_dump(),
        "duration_minutes": payload.duration_minutes,
        "hotel_id": payload.hotel_id,
        "timestamp": datetime.utcnow(),
    }
    result = await breaks.insert_one(doc)
    
    # Update journey with break
    journeys = db.get_collection("Journeys")
    await journeys.update_one(
        {"_id": ObjectId(payload.journey_id)},
        {"$push": {"breaks_taken": doc}}
    )
    
    return BreakRecordResponse(ok=True, break_id=str(result.inserted_id))
