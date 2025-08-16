from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.core.config import settings

mongo_client = None
mongo_db = None

async def connect_to_mongo():
    global mongo_client, mongo_db
    mongo_client = AsyncIOMotorClient(settings.mongo_url)
    mongo_db = mongo_client["skillstacker"]
    
    # Initialize beanie with document models
    from src.db.mongo_models import Review
    await init_beanie(database=mongo_db, document_models=[Review])

async def close_mongo_connection():
    global mongo_client
    if mongo_client:
        mongo_client.close()

def get_mongo_db():
    return mongo_db