from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from bson import ObjectId

from ..core.db import get_database
from ..models.schemas import (
    JourneyStartRequest,
    JourneyStartResponse,
    JourneyTrackRequest,
    JourneyTrackResponse,
    JourneyStopRequest,
    JourneyStopResponse,
)


router = APIRouter(prefix="/journey", tags=["journey"])


@router.post("/start", response_model=JourneyStartResponse)
async def start_journey(
    payload: JourneyStartRequest, db: AsyncIOMotorDatabase = Depends(get_database)
) -> JourneyStartResponse:
    journeys = db.get_collection("Journeys")
    doc: dict[str, Any] = {
        "user_id": payload.user_id,
        "start": payload.start_location.model_dump(),
        "destination": payload.destination.model_dump(),
        "total_distance_km": payload.total_distance_km,
        "start_time": datetime.utcnow(),
        "end_time": None,
        "telemetry": [],
        "breaks_taken": [],
        "sos_triggered": False,
        "status": "active",
    }
    result = await journeys.insert_one(doc)
    return JourneyStartResponse(journey_id=str(result.inserted_id), started_at=doc["start_time"]) 


@router.post("/track", response_model=JourneyTrackResponse)
async def track_journey(
    payload: JourneyTrackRequest, db: AsyncIOMotorDatabase = Depends(get_database)
) -> JourneyTrackResponse:
    journeys = db.get_collection("Journeys")
    update = {
        "$push": {"telemetry": payload.telemetry.model_dump()},
    }
    updated = await journeys.find_one_and_update(
        {"_id": {"$eq": ObjectId(payload.journey_id)}},
        update,
        return_document=ReturnDocument.AFTER,
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found")

    eta: datetime | None = None
    try:
        total_distance = updated.get("total_distance_km")
        if total_distance and updated.get("telemetry"):
            latest = updated["telemetry"][-1]
            covered = latest.get("distance_covered_km")
            speed = latest.get("speed_kmph")
            if covered is not None and speed and speed > 1:
                remaining = max(total_distance - covered, 0)
                # hours = distance / speed
                hours = remaining / float(speed)
                eta = datetime.utcnow() + timedelta(hours=hours)
    except Exception:
        eta = None

    return JourneyTrackResponse(ok=True, eta_iso=eta)


@router.post("/stop", response_model=JourneyStopResponse)
async def stop_journey(
    payload: JourneyStopRequest, db: AsyncIOMotorDatabase = Depends(get_database)
) -> JourneyStopResponse:
    journeys = db.get_collection("Journeys")
    ended_at = datetime.utcnow()
    update = {
        "$set": {
            "end_time": ended_at,
            "status": "completed",
            "end": payload.end_location.model_dump() if payload.end_location else None,
        }
    }
    updated = await journeys.find_one_and_update(
        {"_id": {"$eq": ObjectId(payload.journey_id)}},
        update,
        return_document=ReturnDocument.AFTER,
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found")

    return JourneyStopResponse(ok=True, ended_at=ended_at)


