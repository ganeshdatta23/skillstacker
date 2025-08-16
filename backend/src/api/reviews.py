from fastapi import APIRouter
from typing import List
import logging
from pymongo import MongoClient
from src.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

def get_mongo_db():
    """Get MongoDB database connection"""
    try:
        client = MongoClient(settings.mongo_url)
        return client.skillstacker
    except Exception as e:
        logger.error(f"MongoDB connection error: {e}")
        return None

@router.get("/product/{product_id}")
def get_product_reviews(product_id: int):
    """Get reviews for a specific product"""
    try:
        db = get_mongo_db()
        if db is not None:
            reviews = list(db.reviews.find({"product_id": product_id}))
            # Convert ObjectId to string
            for review in reviews:
                review["id"] = str(review["_id"])
                del review["_id"]
            return reviews
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
    
    # Fallback to mock data
    return [
        {
            "id": "1",
            "product_id": product_id,
            "user_id": 1,
            "rating": 5,
            "title": "Great product!",
            "content": "Really enjoyed this.",
            "created_at": "2024-01-01T00:00:00Z",
            "helpful_count": 5
        }
    ]

@router.get("/product/{product_id}/summary")
def get_product_review_summary(product_id: int):
    """Get review summary for a product"""
    try:
        db = get_mongo_db()
        if db is not None:
            reviews = list(db.reviews.find({"product_id": product_id}))
            if reviews:
                total_reviews = len(reviews)
                avg_rating = sum(r.get("rating", 0) for r in reviews) / total_reviews
                return {
                    "average_rating": round(avg_rating, 1),
                    "total_reviews": total_reviews
                }
    except Exception as e:
        logger.error(f"Error fetching review summary: {e}")
    
    # Fallback data
    return {
        "average_rating": 4.5,
        "total_reviews": 1,
        "rating_distribution": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 1}
    }