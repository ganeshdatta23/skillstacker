from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.dependencies import get_db
from src.db.models import Film as Product
from src.schemas import ProductResponse
import logging
import math

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(1000, ge=1, le=10000, description="Number of records to return (default: all)"),
    search: Optional[str] = Query(None, description="Search term for product name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating filter"),
    db: Session = Depends(get_db)
):
    """Get products with filtering and pagination"""
    try:
        query = db.query(Product)
        
        # Apply filters
        if search:
            search_term = search.strip().replace('%', '\\%').replace('_', '\\_')
            query = query.filter(Product.title.ilike(f"%{search_term}%"))
        
        # Note: Film table doesn't have category field, skip category filter for now
        # if category:
        #     query = query.filter(Product.category == category)
            
        # Note: rating is text field (G, PG, PG-13, R), not numeric
        # if min_rating is not None:
        #     query = query.filter(Product.rating >= min_rating)
        
        # Get total count for pagination
        total = query.count()
        
        # Apply pagination
        products = query.offset(skip).limit(limit).all()
        
        logger.info(f"Retrieved {len(products)} out of {total} total products")
        return products
        
    except Exception as e:
        logger.error(f"Error retrieving products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/all", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    """Get ALL products without any limits - for frontend display"""
    try:
        products = db.query(Product).all()
        logger.info(f"Retrieved ALL {len(products)} products")
        return products
        
    except Exception as e:
        logger.error(f"Error retrieving all products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/stats")
def get_product_stats(db: Session = Depends(get_db)):
    """Get database statistics"""
    try:
        total_products = db.query(Product).count()
        ratings = db.query(Product.rating).distinct().all()
        rating_list = [rating[0] for rating in ratings if rating[0]]
        
        return {
            "total_products": total_products,
            "total_ratings": len(rating_list),
            "ratings": rating_list
        }
    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get all available product categories (ratings)"""
    try:
        ratings = db.query(Product.rating).distinct().all()
        return [rating[0] for rating in ratings if rating[0]]
    except Exception as e:
        logger.error(f"Error retrieving categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    try:
        if product_id <= 0:
            raise HTTPException(status_code=400, detail="Product ID must be positive")
        
        product = db.query(Product).filter(Product.film_id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")