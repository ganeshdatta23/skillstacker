from typing import List
from src.db.mongo_models import Review, ReviewCreate, ReviewUpdate
from datetime import datetime, timezone
from beanie import PydanticObjectId

class ReviewService:
    async def create_review(self, review: ReviewCreate, user_id: int):
        review_doc = Review(
            **review.dict(),
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        await review_doc.insert()
        return str(review_doc.id)
    
    async def get_reviews_by_product(self, product_id: int, skip: int = 0, limit: int = 20):
        reviews = await Review.find(Review.product_id == product_id).skip(skip).limit(limit).sort(-Review.created_at).to_list()
        return reviews
    
    async def update_review(self, review_id: str, review_update: ReviewUpdate, user_id: int):
        review = await Review.find_one(Review.id == PydanticObjectId(review_id), Review.user_id == user_id)
        if not review:
            return False
        
        update_data = {k: v for k, v in review_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.now(timezone.utc)
        
        await review.update({"$set": update_data})
        return True
    
    async def delete_review(self, review_id: str, user_id: int):
        review = await Review.find_one(Review.id == PydanticObjectId(review_id), Review.user_id == user_id)
        if not review:
            return False
        await review.delete()
        return True
    
    async def get_product_rating_summary(self, product_id: int):
        pipeline = [
            {"$match": {"product_id": product_id}},
            {"$group": {
                "_id": "$product_id",
                "average_rating": {"$avg": "$rating"},
                "total_reviews": {"$sum": 1}
            }}
        ]
        result = await Review.aggregate(pipeline).to_list()
        return result[0] if result else None

review_service = ReviewService()