from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.core.dependencies import get_db
from src.db.models import Category
from src.schemas import CategoryResponse

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/all", response_model=List[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/stats")
def get_category_stats(db: Session = Depends(get_db)):
    total_categories = db.query(Category).count()
    return {"total_categories": total_categories}

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category