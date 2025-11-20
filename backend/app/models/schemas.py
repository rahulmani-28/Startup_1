from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Location(BaseModel):
    lat: float
    lon: float
    name: Optional[str] = None


class JourneyStartRequest(BaseModel):
    user_id: str
    start_location: Location
    destination: Location
    total_distance_km: Optional[float] = None


class JourneyStartResponse(BaseModel):
    journey_id: str
    started_at: datetime


class TelemetryPoint(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location: Location
    speed_kmph: float = Field(ge=0)
    distance_covered_km: Optional[float] = None


class JourneyTrackRequest(BaseModel):
    journey_id: str
    telemetry: TelemetryPoint


class JourneyTrackResponse(BaseModel):
    ok: bool
    eta_iso: Optional[datetime] = None


class JourneyStopRequest(BaseModel):
    journey_id: str
    end_location: Optional[Location] = None


class JourneyStopResponse(BaseModel):
    ok: bool
    ended_at: datetime


# --- Breaks ---
class BreakSuggestionRequest(BaseModel):
    journey_id: str
    total_distance_km: float
    elapsed_time_hours: float

class BreakSuggestion(BaseModel):
    should_take_break: bool
    reason: Optional[str] = None
    nearby_hotels_count: int = 0

class BreakRecordRequest(BaseModel):
    journey_id: str
    location: Location
    duration_minutes: int
    hotel_id: Optional[str] = None

class BreakRecordResponse(BaseModel):
    ok: bool
    break_id: str


# --- Hotels ---
class Hotel(BaseModel):
    id: str
    name: str
    location: Location
    tags: List[str] = []  # veg, budget, family
    rating: float = 0.0
    address: Optional[str] = None

class HotelSearchRequest(BaseModel):
    lat: float
    lon: float
    radius_km: float = 5.0

class HotelSearchResponse(BaseModel):
    hotels: List[Hotel]


# --- SOS ---
class SOSAlertRequest(BaseModel):
    journey_id: str
    location: Location
    type: str = "manual"  # manual, auto_crash

class SOSAlertResponse(BaseModel):
    ok: bool
    alert_id: str
    notified_contacts: List[str]
    nearest_police: Optional[Location] = None
    nearest_hospital: Optional[Location] = None


# --- Reviews ---
class ReviewSubmitRequest(BaseModel):
    hotel_id: str
    user_id: str
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None
    tags: List[str] = []

class Review(BaseModel):
    id: str
    hotel_id: str
    user_id: str
    rating: int
    comment: Optional[str]
    timestamp: datetime

class ReviewListResponse(BaseModel):
    reviews: List[Review]


