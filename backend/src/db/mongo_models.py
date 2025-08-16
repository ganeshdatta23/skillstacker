from beanie import Document
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class Review(Document):
    product_id: int
    user_id: int
    rating: int
    title: str
    content: str
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    helpful_count: int = 0
    
    class Settings:
        name = "reviews"

class ReviewCreate(BaseModel):
    product_id: int
    rating: int
    title: str
    content: str

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None

class ReviewResponse(BaseModel):
    id: str
    product_id: int
    user_id: int
    rating: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    helpful_count: int