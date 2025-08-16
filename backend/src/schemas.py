from pydantic import BaseModel, field_serializer, EmailStr
from datetime import datetime, date
from typing import Optional
from decimal import Decimal

# Auth Schemas
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str
    activebool: bool
    is_admin: bool
    oauth_provider: Optional[str] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Film/Product Schemas
class FilmResponse(BaseModel):
    film_id: int
    title: str
    description: Optional[str]
    release_year: Optional[int]
    rental_rate: Decimal
    length: Optional[int]
    rating: Optional[str]
    
    @field_serializer('rental_rate')
    def serialize_rental_rate(self, value: Decimal) -> str:
        return str(value)
    
    class Config:
        from_attributes = True

# Actor Schemas
class ActorResponse(BaseModel):
    actor_id: int
    first_name: str
    last_name: str
    
    class Config:
        from_attributes = True

# Category Schemas
class CategoryResponse(BaseModel):
    category_id: int
    name: str
    
    class Config:
        from_attributes = True

# Language Schemas
class LanguageResponse(BaseModel):
    language_id: int
    name: str
    
    class Config:
        from_attributes = True

# Rental Schemas
class RentalResponse(BaseModel):
    rental_id: int
    customer_id: int
    inventory_id: int
    rental_date: datetime
    return_date: Optional[datetime]
    
    class Config:
        from_attributes = True

class PaymentResponse(BaseModel):
    payment_id: int
    customer_id: int
    rental_id: int
    amount: Decimal
    
    @field_serializer('amount')
    def serialize_amount(self, value: Decimal) -> str:
        return str(value)
    
    class Config:
        from_attributes = True

# Legacy aliases
ProductResponse = FilmResponse
OrderResponse = RentalResponse