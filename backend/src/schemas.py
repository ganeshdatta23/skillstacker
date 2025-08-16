from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserResponse(UserBase):
    customer_id: int
    is_admin: bool = False
    activebool: bool = True
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Product Schemas
class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    rating: Optional[str] = None

class ProductResponse(ProductBase):
    film_id: int
    length: Optional[int] = None
    
    class Config:
        from_attributes = True

# Review Schemas (for MongoDB)
class ReviewBase(BaseModel):
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=2000)

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1, max_length=2000)

class ReviewResponse(ReviewBase):
    id: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    helpful_count: int = 0
    
    class Config:
        from_attributes = True

# Order Schemas
class OrderBase(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(1, gt=0)

class OrderCreate(OrderBase):
    pass

class OrderResponse(BaseModel):
    rental_id: int
    rental_date: datetime
    customer_id: int
    return_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Generic Response Schemas
class MessageResponse(BaseModel):
    message: str
    
class ErrorResponse(BaseModel):
    detail: str