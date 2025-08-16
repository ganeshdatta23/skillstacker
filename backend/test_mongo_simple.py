#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from pymongo import MongoClient
    from src.core.config import settings
    
    def test_mongodb_simple():
        print(f"MongoDB URL: {settings.mongo_url}")
        
        try:
            # Test MongoDB connection
            client = MongoClient(settings.mongo_url, serverSelectionTimeoutMS=5000)
            
            # Test connection
            client.admin.command('ping')
            print("[OK] MongoDB connection successful")
            
            # List databases
            db_list = client.list_database_names()
            print(f"[OK] Available databases: {db_list}")
            
            # Test skillstacker database
            db = client.skillstacker
            collections = db.list_collection_names()
            print(f"[OK] Collections in skillstacker db: {collections}")
            
            # Test reviews collection
            if 'reviews' in collections:
                reviews_count = db.reviews.count_documents({})
                print(f"[OK] Found {reviews_count} reviews in database")
                
                if reviews_count > 0:
                    sample = db.reviews.find_one()
                    print(f"[OK] Sample review: {sample}")
            else:
                print("[WARNING] No reviews collection found")
                print("[INFO] Creating sample review data...")
                
                # Insert sample review
                sample_review = {
                    "product_id": 1,
                    "user_id": 1,
                    "rating": 5,
                    "title": "Great product!",
                    "content": "Really enjoyed this product.",
                    "created_at": "2024-01-01T00:00:00Z",
                    "helpful_count": 5
                }
                result = db.reviews.insert_one(sample_review)
                print(f"[OK] Inserted sample review with ID: {result.inserted_id}")
                
            client.close()
            
        except Exception as e:
            print(f"[ERROR] MongoDB error: {e}")
            
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    print("[INFO] Installing pymongo...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "pymongo"])

if __name__ == "__main__":
    test_mongodb_simple()