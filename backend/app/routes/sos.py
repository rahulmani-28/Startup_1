from datetime import datetime
from typing import Optional
import httpx

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from ..core.db import get_database
from ..models.schemas import SOSAlertRequest, SOSAlertResponse, Location

router = APIRouter(prefix="/sos", tags=["sos"])

@router.post("/alert", response_model=SOSAlertResponse)
async def trigger_sos(
    payload: SOSAlertRequest, db: AsyncIOMotorDatabase = Depends(get_database)
) -> SOSAlertResponse:
    sos_logs = db.get_collection("SOSLogs")
    
    # Fetch nearest police and hospital from OSM
    police = None
    hospital = None
    
    try:
        async with httpx.AsyncClient() as client:
            query = f"""
            [out:json];
            (
              node["amenity"="police"](around:5000,{payload.location.lat},{payload.location.lon});
              node["amenity"="hospital"](around:5000,{payload.location.lat},{payload.location.lon});
            );
            out center;
            """
            resp = await client.post("https://overpass-api.de/api/interpreter", data={"data": query}, timeout=10.0)
            if resp.status_code == 200:
                elements = resp.json().get("elements", [])
                for el in elements:
                    tags = el.get("tags", {})
                    amenity = tags.get("amenity")
                    loc = Location(lat=el.get("lat"), lon=el.get("lon"), name=tags.get("name", f"Nearby {amenity}"))
                    
                    if amenity == "police" and not police:
                        police = loc
                    elif amenity == "hospital" and not hospital:
                        hospital = loc
    except Exception as e:
        print(f"OSM SOS Error: {e}")

    doc = {
        "journey_id": payload.journey_id,
        "location": payload.location.model_dump(),
        "type": payload.type,
        "timestamp": datetime.utcnow(),
        "notified": ["Police", "Hospital", "Emergency Contacts"],
        "nearest_police": police.model_dump() if police else None,
        "nearest_hospital": hospital.model_dump() if hospital else None,
    }
    
    result = await sos_logs.insert_one(doc)
    
    # Update journey
    journeys = db.get_collection("Journeys")
    await journeys.update_one(
        {"_id": ObjectId(payload.journey_id)},
        {"$set": {"sos_triggered": True}}
    )
    
    return SOSAlertResponse(
        ok=True,
        alert_id=str(result.inserted_id),
        notified_contacts=["+91-9876543210", "100", "108"],
        nearest_police=police,
        nearest_hospital=hospital
    )
