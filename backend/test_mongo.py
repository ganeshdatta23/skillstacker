#!/usr/bin/env python3
import sys
import asyncio
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

async def test_mongodb():
    print(f"MongoDB URL: {settings.mongo_url}")
    
    try:
        # Test MongoDB connection
        client = AsyncIOMotorClient(settings.mongo_url)
        
        # Test connection by listing databases
        db_list = await client.list_database_names()
        print(f"[OK] MongoDB connection successful")
        print(f"[OK] Available databases: {db_list}")
        
        # Test skillstacker database
        db = client.skillstacker
        collections = await db.list_collection_names()
        print(f"[OK] Collections in skillstacker db: {collections}")
        
        # Test reviews collection
        if 'reviews' in collections:
            reviews_count = await db.reviews.count_documents({})
            print(f"[OK] Found {reviews_count} reviews in database")
            
            if reviews_count > 0:
                sample = await db.reviews.find_one()
                print(f"[OK] Sample review: {sample}")
        else:
            print("[WARNING] No reviews collection found")
            
        client.close()
        
    except Exception as e:
        print(f"[ERROR] MongoDB error: {e}")
        print("[INFO] This is expected if MongoDB is not running")

if __name__ == "__main__":
    asyncio.run(test_mongodb())