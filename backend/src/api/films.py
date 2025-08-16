from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.dependencies import get_db
from src.db.models import Film
from src.schemas import FilmResponse

router = APIRouter()

@router.get("/", response_model=List[FilmResponse])
def get_films(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=10000),
    search: Optional[str] = Query(None, description="Search in title or description"),
    rating: Optional[str] = Query(None, description="Filter by rating (G, PG, PG-13, R, NC-17)"),
    min_year: Optional[int] = Query(None, description="Minimum release year"),
    max_year: Optional[int] = Query(None, description="Maximum release year"),
    db: Session = Depends(get_db)
):
    """Get films with filtering and pagination - shows ALL 1000 films by default"""
    query = db.query(Film)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Film.title.ilike(search_term)) | 
            (Film.description.ilike(search_term))
        )
    
    if rating:
        query = query.filter(Film.rating == rating)
    
    if min_year:
        query = query.filter(Film.release_year >= min_year)
    
    if max_year:
        query = query.filter(Film.release_year <= max_year)
    
    total = query.count()
    films = query.offset(skip).limit(limit).all()
    
    return films

@router.get("/all", response_model=List[FilmResponse])
def get_all_films(db: Session = Depends(get_db)):
    """Get ALL 1000 films without any pagination"""
    return db.query(Film).all()

@router.get("/stats")
def get_film_stats(db: Session = Depends(get_db)):
    """Get comprehensive film statistics"""
    total_films = db.query(Film).count()
    
    # Get all ratings
    ratings = db.query(Film.rating).distinct().all()
    rating_counts = {}
    for rating in ratings:
        if rating[0]:
            count = db.query(Film).filter(Film.rating == rating[0]).count()
            rating_counts[rating[0]] = count
    
    # Get year range
    years = db.query(Film.release_year).filter(Film.release_year.isnot(None)).all()
    year_list = [y[0] for y in years if y[0]]
    
    return {
        "total_films": total_films,
        "ratings": rating_counts,
        "year_range": {
            "min": min(year_list) if year_list else None,
            "max": max(year_list) if year_list else None
        },
        "avg_rental_rate": float(db.query(Film.rental_rate).filter(Film.rental_rate.isnot(None)).all()[0][0]) if total_films > 0 else 0
    }

@router.get("/{film_id}", response_model=FilmResponse)
def get_film(film_id: int, db: Session = Depends(get_db)):
    """Get a specific film by ID"""
    film = db.query(Film).filter(Film.film_id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film