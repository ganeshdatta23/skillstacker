from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.db.postgres import get_db
from src.db.models import Film
from src.schemas import ProductResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search term for product title"),
    rating: Optional[str] = Query(None, description="Filter by rating"),
    db: Session = Depends(get_db)
):
    """
    Retrieve products with pagination, search, and filtering.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (1-100)
    - **search**: Search term to filter by product title
    - **rating**: Filter by specific rating (G, PG, PG-13, R, NC-17)
    """
    try:
        query = db.query(Film)
        
        # Apply search filter
        if search:
            # Sanitize search input to prevent SQL injection
            search_term = search.strip().replace('%', '\\%').replace('_', '\\_')
            query = query.filter(Film.title.ilike(f"%{search_term}%"))
        
        # Apply rating filter
        if rating:
            # Validate rating input
            valid_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17']
            if rating not in valid_ratings:
                raise HTTPException(status_code=400, detail=f"Invalid rating. Must be one of: {valid_ratings}")
            query = query.filter(Film.rating == rating)
        
        # Apply pagination
        products = query.offset(skip).limit(limit).all()
        
        logger.info(f"Retrieved {len(products)} products with filters applied")
        return products
        
    except Exception as e:
        logger.error(f"Error retrieving products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific product by ID.
    
    - **product_id**: The ID of the product to retrieve
    """
    try:
        # Validate product_id
        if product_id <= 0:
            raise HTTPException(status_code=400, detail="Product ID must be a positive integer")
        
        product = db.query(Film).filter(Film.film_id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        logger.info(f"Retrieved product with ID: {product_id}")
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving product with ID: {product_id}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}/stats")
def get_product_stats(product_id: int, db: Session = Depends(get_db)):
    """
    Get statistics for a specific product.
    
    - **product_id**: The ID of the product
    """
    try:
        # Validate product exists
        product = db.query(Film).filter(Film.film_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # TODO: Add review statistics from MongoDB
        stats = {
            "product_id": product_id,
            "title": product.title,
            "rating": product.rating,
            "length": product.length,
            "total_reviews": 0,  # Will be populated from MongoDB
            "average_rating": 0.0,  # Will be calculated from reviews
            "rating_distribution": {}  # Will show distribution of ratings
        }
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving product stats for ID: {product_id}")
        raise HTTPException(status_code=500, detail="Internal server error")