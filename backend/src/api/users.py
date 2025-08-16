from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from src.db.postgres import get_db
from src.core.dependencies import get_current_active_user
from src.db.models import User
from src.schemas import UserResponse, UserCreate
from typing import List

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    token: str = Depends(security)
):
    return db.query(User).all()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    token: str = Depends(security)
):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    user = db.query(User).filter(User.customer_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Note: User creation is now handled by /auth/register endpoint
# This endpoint is kept for admin purposes
@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    token: str = Depends(security)
):
    # Only admins can create users directly
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    from src.core.security import get_password_hash
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        activebool=True,
        active=1
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
