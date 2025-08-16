from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from typing import Optional

_client: Optional[AsyncIOMotorClient] = None

async def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongo_url)
    return _client

async def close_mongo_client():
    global _client
    if _client:
        _client.close()
        _client = None