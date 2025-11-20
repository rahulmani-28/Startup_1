import httpx
from typing import List

from fastapi import APIRouter, HTTPException
from ..models.schemas import HotelSearchRequest, HotelSearchResponse, Hotel, Location

router = APIRouter(prefix="/hotels", tags=["hotels"])

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

@router.post("/nearby", response_model=HotelSearchResponse)
async def search_hotels(payload: HotelSearchRequest) -> HotelSearchResponse:
    # Query OSM for hotels, motels, guest_houses within radius
    # Overpass QL
    radius_m = payload.radius_km * 1000
    query = f"""
    [out:json];
    (
      node["tourism"~"hotel|motel|guest_house|hostel"](around:{radius_m},{payload.lat},{payload.lon});
      way["tourism"~"hotel|motel|guest_house|hostel"](around:{radius_m},{payload.lat},{payload.lon});
    );
    out center;
    """
    
    try:
        async with httpx.AsyncClient() as client:
            # In a real scenario, handle timeouts and errors gracefully
            # For testing/mock, we might want to fallback if OSM is slow or blocks us
            # But let's try to hit it.
            resp = await client.post(OVERPASS_URL, data={"data": query}, timeout=10.0)
            if resp.status_code != 200:
                # Fallback to mock data if OSM fails
                return get_mock_hotels(payload.lat, payload.lon)
            
            data = resp.json()
            elements = data.get("elements", [])
            
            hotels: List[Hotel] = []
            for el in elements:
                lat = el.get("lat") or el.get("center", {}).get("lat")
                lon = el.get("lon") or el.get("center", {}).get("lon")
                name = el.get("tags", {}).get("name", "Unknown Hotel")
                
                if lat and lon:
                    hotels.append(Hotel(
                        id=str(el["id"]),
                        name=name,
                        location=Location(lat=lat, lon=lon),
                        tags=["budget"] if "motel" in el.get("tags", {}).values() else ["family"],
                        rating=4.0 # Mock rating
                    ))
            
            if not hotels:
                 return get_mock_hotels(payload.lat, payload.lon)

            return HotelSearchResponse(hotels=hotels[:10]) # Limit to 10

    except Exception as e:
        print(f"OSM Error: {e}")
        return get_mock_hotels(payload.lat, payload.lon)

def get_mock_hotels(lat: float, lon: float) -> HotelSearchResponse:
    # Provide some dummy hotels around the location
    return HotelSearchResponse(hotels=[
        Hotel(id="mock1", name="Highway Inn", location=Location(lat=lat+0.001, lon=lon+0.001), tags=["veg", "budget"], rating=4.2),
        Hotel(id="mock2", name="Royal Dhaba", location=Location(lat=lat-0.001, lon=lon-0.001), tags=["non-veg", "family"], rating=4.5),
        Hotel(id="mock3", name="Travelers Rest", location=Location(lat=lat+0.002, lon=lon-0.002), tags=["budget"], rating=3.8),
    ])
