from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from .config import settings


mongo_client: AsyncIOMotorClient | None = None
database: AsyncIOMotorDatabase | None = None


async def get_database() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    if database is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo() at startup.")
    yield database


async def connect_to_mongo() -> None:
    global mongo_client, database
    mongo_client = AsyncIOMotorClient(settings.mongodb_uri)
    database = mongo_client[settings.database_name]


async def close_mongo_connection() -> None:
    global mongo_client
    if mongo_client is not None:
        mongo_client.close()
        mongo_client = None


