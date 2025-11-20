from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from ..core.db import get_database
from ..models.schemas import ReviewSubmitRequest, Review, ReviewListResponse

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=Review)
async def submit_review(
    payload: ReviewSubmitRequest, db: AsyncIOMotorDatabase = Depends(get_database)
) -> Review:
    reviews = db.get_collection("Reviews")
    doc = {
        "hotel_id": payload.hotel_id,
        "user_id": payload.user_id,
        "rating": payload.rating,
        "comment": payload.comment,
        "tags": payload.tags,
        "timestamp": datetime.utcnow(),
    }
    result = await reviews.insert_one(doc)
    
    return Review(
        id=str(result.inserted_id),
        **doc
    )

@router.get("/hotel/{hotel_id}", response_model=ReviewListResponse)
async def get_hotel_reviews(
    hotel_id: str, db: AsyncIOMotorDatabase = Depends(get_database)
) -> ReviewListResponse:
    reviews_coll = db.get_collection("Reviews")
    cursor = reviews_coll.find({"hotel_id": hotel_id})
    
    results = []
    async for doc in cursor:
        results.append(Review(
            id=str(doc["_id"]),
            hotel_id=doc["hotel_id"],
            user_id=doc["user_id"],
            rating=doc["rating"],
            comment=doc.get("comment"),
            timestamp=doc["timestamp"]
        ))
        
    return ReviewListResponse(reviews=results)
