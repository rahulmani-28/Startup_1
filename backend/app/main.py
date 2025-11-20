from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.db import connect_to_mongo, close_mongo_connection
from .routes.journey import router as journey_router
from .routes.breaks import router as breaks_router
from .routes.hotels import router as hotels_router
from .routes.sos import router as sos_router
from .routes.reviews import router as reviews_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(journey_router)
app.include_router(breaks_router)
app.include_router(hotels_router)
app.include_router(sos_router)
app.include_router(reviews_router)

@app.get("/")
async def root():
    return {"status": "ok", "service": settings.app_name}


