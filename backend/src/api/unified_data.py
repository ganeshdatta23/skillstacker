# =============================================================================
# UNIFIED DATA API - COMPREHENSIVE CRUD OPERATIONS
# =============================================================================
# This file contains all CRUD (Create, Read, Update, Delete) operations
# for the SkillStacker platform, working with both PostgreSQL and MongoDB
# 
# What this file does:
# 1. Provides unified search across all data sources
# 2. Handles CRUD operations for Films, Actors, and Reviews
# 3. Manages bulk operations for efficiency
# 4. Provides statistics and analytics
# =============================================================================

# Import necessary libraries
from fastapi import APIRouter, Depends, HTTPException, Query  # FastAPI components
from sqlalchemy.orm import Session  # Database session management
from typing import List, Optional, Dict, Any, Union  # Type hints for better code
import logging  # For error tracking and debugging
import re  # Regular expressions for text processing
from datetime import datetime  # Date and time handling
from pymongo import MongoClient  # MongoDB connection

# Import our custom modules
from src.core.dependencies import get_db  # Database dependency injection
from src.core.config import settings  # Application settings
from src.db.models import Film, Actor, Category, User, Rental, Payment  # PostgreSQL models
from src.schemas import FilmResponse, ActorResponse, CategoryResponse, UserResponse  # Data validation schemas

# Create router instance - this groups all our API endpoints together
router = APIRouter()

# Set up logging - helps us track what's happening in our application
logger = logging.getLogger(__name__)

def get_mongo_db():
    """
    Connect to MongoDB database safely
    
    This function:
    1. Creates a connection to MongoDB using our settings
    2. Tests the connection with a 'ping' command
    3. Returns the database if successful, None if failed
    4. Logs any errors for debugging
    
    Returns:
        MongoDB database object or None if connection fails
    """
    try:
        # Create MongoDB client with 5-second timeout
        client = MongoClient(settings.mongo_url, serverSelectionTimeoutMS=5000)
        
        # Test if MongoDB is actually reachable
        client.admin.command('ping')
        
        # Return our specific database
        return client.skillstacker
    except Exception as e:
        # Log the error so we can debug connection issues
        logger.error(f"MongoDB connection error: {e}")
        return None

def sanitize_search_term(term: str) -> str:
    """
    Clean up search terms to make them safe
    
    This function protects our application from malicious input by:
    1. Checking if the term exists
    2. Removing dangerous characters that could break our database
    3. Limiting the length to prevent abuse
    
    Args:
        term (str): The search term from the user
        
    Returns:
        str: A clean, safe version of the search term
    """
    # If no search term provided, return empty string
    if not term:
        return ""
    
    # Remove special characters that could be used for attacks
    # Keep only: letters, numbers, spaces, and hyphens
    # Limit to 100 characters to prevent very long searches
    sanitized = re.sub(r'[^\w\s-]', '', term.strip())[:100]
    return sanitized

@router.get("/search")
def unified_search(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category (films, actors, users, publications, reviews)"),
    limit: int = Query(50, ge=1, le=200, description="Number of results to return"),
    skip: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """
    🔍 UNIFIED SEARCH - Search across all our databases at once!
    
    This is like having a Google search for our entire application.
    It searches through:
    - Films (movies in PostgreSQL)
    - Actors (people in PostgreSQL) 
    - Users (customers in PostgreSQL)
    - Publications (articles in MongoDB)
    - Reviews (user reviews in MongoDB)
    
    Parameters:
        q: What you want to search for (required)
        category: Limit search to specific type (optional)
        limit: How many results to return (1-200, default 50)
        skip: How many results to skip (for pagination)
        db: Database connection (automatically provided)
        
    Returns:
        JSON with search results organized by category
    """
    try:
        # Step 1: Clean the search term to make it safe
        search_term = sanitize_search_term(q)
        if not search_term:
            raise HTTPException(status_code=400, detail="Invalid search term")
        
        # Step 2: Prepare our results container
        # This will hold all the search results organized by type
        results = {
            "query": q,  # What the user searched for
            "total_results": 0,  # Total number of results found
            "films": [],  # Movies/films found
            "actors": [],  # Actors found
            "users": [],  # Users found
            "publications": [],  # Articles/publications found
            "reviews": []  # User reviews found
        }
        
        # Step 3: Search Films (PostgreSQL Database)
        # Only search films if no category specified OR category is "films"
        if not category or category == "films":
            # Query the database for films with titles containing our search term
            # ilike = case-insensitive search ("Movie" matches "movie")
            films = db.query(Film).filter(
                Film.title.ilike(f"%{search_term}%")
            ).offset(skip).limit(limit).all()
            
            # Convert database objects to simple dictionaries for JSON response
            results["films"] = [
                {
                    "id": f.film_id,
                    "title": f.title,
                    "description": f.description,
                    "rating": f.rating,
                    "length": f.length,
                    "type": "film"
                } for f in films  # List comprehension - creates a list from database results
            ]
        
        # Step 4: Search Actors (PostgreSQL Database)
        if not category or category == "actors":
            # Search both first name AND last name
            # The | symbol means "OR" - match either first name OR last name
            actors = db.query(Actor).filter(
                (Actor.first_name.ilike(f"%{search_term}%")) |
                (Actor.last_name.ilike(f"%{search_term}%"))
            ).offset(skip).limit(limit).all()
            
            # Convert to JSON-friendly format
            results["actors"] = [
                {
                    "id": a.actor_id,
                    "name": f"{a.first_name} {a.last_name}",  # Combine first and last name
                    "first_name": a.first_name,
                    "last_name": a.last_name,
                    "type": "actor"
                } for a in actors
            ]
        
        # Step 5: Search Users (PostgreSQL Database)
        if not category or category == "users":
            # Search in first name, last name, OR email address
            users = db.query(User).filter(
                (User.first_name.ilike(f"%{search_term}%")) |
                (User.last_name.ilike(f"%{search_term}%")) |
                (User.email.ilike(f"%{search_term}%"))
            ).offset(skip).limit(limit).all()
            
            # Convert to JSON format
            results["users"] = [
                {
                    "id": u.customer_id,
                    "name": f"{u.first_name} {u.last_name}",
                    "email": u.email,
                    "active": u.activebool,  # Whether user account is active
                    "type": "user"
                } for u in users
            ]
        
        # Step 6: Search Publications (MongoDB)
        if not category or category == "publications":
            try:
                # Connect directly to MongoDB with proper database/collection structure
                client = MongoClient(settings.mongo_url, serverSelectionTimeoutMS=5000)
                
                # Try different possible database and collection combinations
                publications = []
                
                # Option 1: skillstacker.publications
                try:
                    db = client.skillstacker
                    publications = list(db.publications.find(
                        {"$or": [
                            {"title": {"$regex": search_term, "$options": "i"}},
                            {"content": {"$regex": search_term, "$options": "i"}}
                        ]}
                    ).skip(skip).limit(limit))
                except:
                    pass
                
                # Option 2: Publications-data.Publications
                if not publications:
                    try:
                        db = client["Publications-data"]
                        publications = list(db["Publications"].find(
                            {"title": {"$regex": search_term, "$options": "i"}}
                        ).skip(skip).limit(limit))
                    except:
                        pass
                
                # Option 3: Any database with 'publications' collection
                if not publications:
                    try:
                        for db_name in client.list_database_names():
                            if db_name not in ['admin', 'local', 'config']:
                                db = client[db_name]
                                for collection_name in db.list_collection_names():
                                    if 'publication' in collection_name.lower():
                                        publications = list(db[collection_name].find(
                                            {"$or": [
                                                {"title": {"$regex": search_term, "$options": "i"}},
                                                {"content": {"$regex": search_term, "$options": "i"}}
                                            ]}
                                        ).skip(skip).limit(limit))
                                        if publications:
                                            break
                                if publications:
                                    break
                    except:
                        pass
                
                results["publications"] = [
                    {
                        "id": str(p["_id"]),
                        "title": p.get("title", ""),
                        "content": p.get("content", "")[:200] + "..." if p.get("content") and len(p.get("content", "")) > 200 else p.get("content", ""),
                        "type": p.get("type", "publication"),
                        "groups": p.get("groups", [])
                    } for p in publications
                ]
                
            except Exception as e:
                logger.error(f"MongoDB publications search error: {e}")
                results["publications"] = []
        
        # Search Reviews (MongoDB)
        if not category or category == "reviews":
            mongo_db = get_mongo_db()
            if mongo_db is not None:
                try:
                    reviews = list(mongo_db.reviews.find(
                        {"$or": [
                            {"title": {"$regex": search_term, "$options": "i"}},
                            {"content": {"$regex": search_term, "$options": "i"}}
                        ]},
                        {"_id": 1, "title": 1, "content": 1, "rating": 1, "product_id": 1}
                    ).skip(skip).limit(limit))
                    
                    results["reviews"] = [
                        {
                            "id": str(r["_id"]),
                            "title": r.get("title", ""),
                            "content": r.get("content", "")[:200] + "..." if len(r.get("content", "")) > 200 else r.get("content", ""),
                            "rating": r.get("rating", 0),
                            "product_id": r.get("product_id"),
                            "type": "review"
                        } for r in reviews
                    ]
                except Exception as e:
                    logger.error(f"MongoDB reviews search error: {e}")
        
        # Calculate total results
        results["total_results"] = (
            len(results["films"]) + 
            len(results["actors"]) + 
            len(results["users"]) + 
            len(results["publications"]) + 
            len(results["reviews"])
        )
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unified search error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

@router.get("/stats")
def get_unified_stats(db: Session = Depends(get_db)):
    """Get comprehensive statistics from all data sources"""
    try:
        stats = {
            "postgresql": {
                "films": db.query(Film).count(),
                "actors": db.query(Actor).count(),
                "categories": db.query(Category).count(),
                "users": db.query(User).count(),
                "rentals": db.query(Rental).count(),
                "payments": db.query(Payment).count()
            },
            "mongodb": {
                "publications": 0,
                "reviews": 0
            }
        }
        
        # Get MongoDB stats
        mongo_db = get_mongo_db()
        if mongo_db is not None:
            try:
                # Publications - search all possible locations
                try:
                    client = MongoClient(settings.mongo_url)
                    pub_count = 0
                    
                    # Check all databases and collections for publications
                    for db_name in client.list_database_names():
                        if db_name not in ['admin', 'local', 'config']:
                            db = client[db_name]
                            for collection_name in db.list_collection_names():
                                if 'publication' in collection_name.lower():
                                    pub_count += db[collection_name].count_documents({})
                    
                    stats["mongodb"]["publications"] = pub_count
                except:
                    stats["mongodb"]["publications"] = 0
                
                # Reviews from skillstacker database
                stats["mongodb"]["reviews"] = mongo_db.reviews.count_documents({})
            except Exception as e:
                logger.error(f"MongoDB stats error: {e}")
        
        stats["total"] = (
            stats["postgresql"]["films"] +
            stats["postgresql"]["actors"] +
            stats["postgresql"]["users"] +
            stats["mongodb"]["publications"] +
            stats["mongodb"]["reviews"]
        )
        
        return stats
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")

@router.get("/debug/mongodb")
def debug_mongodb():
    """Debug endpoint to see what's in MongoDB"""
    try:
        client = MongoClient(settings.mongo_url, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        debug_info = {
            "connection": "success",
            "databases": [],
            "collections_found": []
        }
        
        for db_name in client.list_database_names():
            if db_name not in ['admin', 'local', 'config']:
                db = client[db_name]
                collections = db.list_collection_names()
                debug_info["databases"].append({
                    "name": db_name,
                    "collections": collections
                })
                
                for collection_name in collections:
                    count = db[collection_name].count_documents({})
                    sample = list(db[collection_name].find().limit(1))
                    debug_info["collections_found"].append({
                        "database": db_name,
                        "collection": collection_name,
                        "count": count,
                        "sample_fields": list(sample[0].keys()) if sample else []
                    })
        
        return debug_info
        
    except Exception as e:
        return {
            "connection": "failed",
            "error": str(e),
            "mongo_url": settings.mongo_url
        }

@router.get("/categories")
def get_all_categories(db: Session = Depends(get_db)):
    """Get all available categories from all data sources"""
    try:
        categories = {
            "film_ratings": [],
            "film_categories": [],
            "publication_types": [],
            "publication_groups": []
        }
        
        # Film ratings
        ratings = db.query(Film.rating).distinct().all()
        categories["film_ratings"] = [r[0] for r in ratings if r[0]]
        
        # Film categories (from category table)
        film_categories = db.query(Category.name).all()
        categories["film_categories"] = [c[0] for c in film_categories]
        
        # MongoDB categories
        mongo_db = get_mongo_db()
        if mongo_db is not None:
            try:
                # Publication types and groups - search all collections
                try:
                    client = MongoClient(settings.mongo_url)
                    pub_types = set()
                    pub_groups = set()
                    
                    for db_name in client.list_database_names():
                        if db_name not in ['admin', 'local', 'config']:
                            db = client[db_name]
                            for collection_name in db.list_collection_names():
                                if 'publication' in collection_name.lower():
                                    try:
                                        types = db[collection_name].distinct("type")
                                        groups = db[collection_name].distinct("groups")
                                        pub_types.update(types)
                                        pub_groups.update([g for g in groups if g])
                                    except:
                                        pass
                    
                    categories["publication_types"] = list(pub_types)
                    categories["publication_groups"] = list(pub_groups)
                except:
                    categories["publication_types"] = []
                    categories["publication_groups"] = []
            except Exception as e:
                logger.error(f"MongoDB categories error: {e}")
        
        return categories
        
    except Exception as e:
        logger.error(f"Categories error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get categories")

# =============================================================================
# CRUD OPERATIONS FOR FILMS (PostgreSQL)
# =============================================================================
# These functions handle Create, Read, Update, Delete operations for films
# Films are stored in PostgreSQL database for structured data

@router.post("/films")
def create_film(
    title: str,
    description: Optional[str] = None,
    release_year: Optional[int] = None,
    rental_rate: float = 4.99,
    length: Optional[int] = None,
    rating: Optional[str] = "G",
    db: Session = Depends(get_db)
):
    """
    📽️ CREATE FILM - Add a new movie to our database
    
    This function:
    1. Takes film information from the user
    2. Creates a new Film object
    3. Saves it to PostgreSQL database
    4. Returns success message with film ID
    
    Parameters:
        title: Movie title (required)
        description: Movie plot/description (optional)
        release_year: Year the movie was released (optional)
        rental_rate: How much it costs to rent (default: $4.99)
        length: Movie duration in minutes (optional)
        rating: Age rating like G, PG, R (default: "G")
        db: Database connection (automatically provided)
        
    Returns:
        JSON with new film ID and success message
    """
    try:
        # Step 1: Create a new Film object with the provided data
        film = Film(
            title=title,
            description=description,
            release_year=release_year,
            rental_rate=rental_rate,
            length=length,
            rating=rating,
            language_id=1  # Default to English (ID 1 in language table)
        )
        
        # Step 2: Add the film to the database session
        db.add(film)
        
        # Step 3: Save changes to database (commit the transaction)
        db.commit()
        
        # Step 4: Refresh to get the auto-generated ID
        db.refresh(film)
        
        # Step 5: Return success response
        return {
            "id": film.film_id, 
            "title": film.title, 
            "message": "Film created successfully"
        }
    except Exception as e:
        # If anything goes wrong, undo the changes
        db.rollback()
        logger.error(f"Create film error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create film")

@router.get("/films/{film_id}")
def get_film(film_id: int, db: Session = Depends(get_db)):
    """
    🔍 READ FILM - Get details of a specific movie
    
    This function:
    1. Searches for a film by its ID
    2. Returns all film details if found
    3. Returns 404 error if film doesn't exist
    
    Parameters:
        film_id: The unique ID of the film to retrieve
        db: Database connection (automatically provided)
        
    Returns:
        JSON with all film details
    """
    # Step 1: Search for the film in the database
    film = db.query(Film).filter(Film.film_id == film_id).first()
    
    # Step 2: Check if film exists
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Step 3: Return film details as JSON
    return {
        "id": film.film_id,
        "title": film.title,
        "description": film.description,
        "release_year": film.release_year,
        "rental_rate": str(film.rental_rate),  # Convert decimal to string for JSON
        "length": film.length,
        "rating": film.rating
    }

@router.put("/films/{film_id}")
def update_film(
    film_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    release_year: Optional[int] = None,
    rental_rate: Optional[float] = None,
    length: Optional[int] = None,
    rating: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    ✏️ UPDATE FILM - Modify an existing movie's details
    
    This function:
    1. Finds the film by ID
    2. Updates only the fields that are provided
    3. Saves changes to database
    4. Returns success message
    
    Parameters:
        film_id: ID of film to update
        title: New title (optional)
        description: New description (optional)
        release_year: New release year (optional)
        rental_rate: New rental price (optional)
        length: New duration (optional)
        rating: New age rating (optional)
        db: Database connection (automatically provided)
        
    Returns:
        JSON success message
    """
    try:
        # Step 1: Find the film to update
        film = db.query(Film).filter(Film.film_id == film_id).first()
        if not film:
            raise HTTPException(status_code=404, detail="Film not found")
        
        # Step 2: Update only the fields that were provided
        # This allows partial updates - user can change just title, or just rating, etc.
        if title: film.title = title
        if description: film.description = description
        if release_year: film.release_year = release_year
        if rental_rate: film.rental_rate = rental_rate
        if length: film.length = length
        if rating: film.rating = rating
        
        # Step 3: Save changes to database
        db.commit()
        return {"message": "Film updated successfully"}
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        # Handle any other errors
        db.rollback()
        logger.error(f"Update film error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update film")

@router.delete("/films/{film_id}")
def delete_film(film_id: int, db: Session = Depends(get_db)):
    """
    🗑️ DELETE FILM - Remove a movie from our database
    
    This function:
    1. Finds the film by ID
    2. Removes it from the database
    3. Returns success message
    
    ⚠️ WARNING: This permanently deletes the film!
    
    Parameters:
        film_id: ID of film to delete
        db: Database connection (automatically provided)
        
    Returns:
        JSON success message
    """
    try:
        # Step 1: Find the film to delete
        film = db.query(Film).filter(Film.film_id == film_id).first()
        if not film:
            raise HTTPException(status_code=404, detail="Film not found")
        
        # Step 2: Delete the film from database
        db.delete(film)
        
        # Step 3: Save changes (commit the deletion)
        db.commit()
        return {"message": "Film deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        # If deletion fails, rollback to prevent partial deletion
        db.rollback()
        logger.error(f"Delete film error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete film")

# =============================================================================
# CRUD OPERATIONS FOR ACTORS (PostgreSQL)
# =============================================================================
# These functions handle Create, Read, Update, Delete operations for actors
# Actors are people who appear in films, stored in PostgreSQL
@router.post("/actors")
def create_actor(
    first_name: str,
    last_name: str,
    db: Session = Depends(get_db)
):
    """Create a new actor"""
    try:
        actor = Actor(first_name=first_name, last_name=last_name)
        db.add(actor)
        db.commit()
        db.refresh(actor)
        return {"id": actor.actor_id, "name": f"{actor.first_name} {actor.last_name}", "message": "Actor created successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Create actor error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create actor")

@router.get("/actors/{actor_id}")
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    """Get a specific actor by ID"""
    actor = db.query(Actor).filter(Actor.actor_id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return {
        "id": actor.actor_id,
        "first_name": actor.first_name,
        "last_name": actor.last_name,
        "full_name": f"{actor.first_name} {actor.last_name}"
    }

@router.put("/actors/{actor_id}")
def update_actor(
    actor_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update an actor"""
    try:
        actor = db.query(Actor).filter(Actor.actor_id == actor_id).first()
        if not actor:
            raise HTTPException(status_code=404, detail="Actor not found")
        
        if first_name: actor.first_name = first_name
        if last_name: actor.last_name = last_name
        
        db.commit()
        return {"message": "Actor updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Update actor error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update actor")

@router.delete("/actors/{actor_id}")
def delete_actor(actor_id: int, db: Session = Depends(get_db)):
    """Delete an actor"""
    try:
        actor = db.query(Actor).filter(Actor.actor_id == actor_id).first()
        if not actor:
            raise HTTPException(status_code=404, detail="Actor not found")
        
        db.delete(actor)
        db.commit()
        return {"message": "Actor deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Delete actor error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete actor")

# CRUD Operations for Reviews (MongoDB)
@router.post("/reviews")
def create_review(
    title: str,
    content: str,
    rating: int = Query(..., ge=1, le=5),
    product_id: Optional[int] = None,
    user_id: Optional[int] = None
):
    """Create a new review in MongoDB"""
    try:
        mongo_db = get_mongo_db()
        if mongo_db is None:
            raise HTTPException(status_code=503, detail="MongoDB unavailable")
        
        review = {
            "title": title,
            "content": content,
            "rating": rating,
            "product_id": product_id,
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = mongo_db.reviews.insert_one(review)
        return {
            "id": str(result.inserted_id),
            "title": title,
            "rating": rating,
            "message": "Review created successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create review error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create review")

@router.get("/reviews/{review_id}")
def get_review(review_id: str):
    """Get a specific review by ID"""
    try:
        mongo_db = get_mongo_db()
        if mongo_db is None:
            raise HTTPException(status_code=503, detail="MongoDB unavailable")
        
        from bson import ObjectId
        review = mongo_db.reviews.find_one({"_id": ObjectId(review_id)})
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        return {
            "id": str(review["_id"]),
            "title": review.get("title", ""),
            "content": review.get("content", ""),
            "rating": review.get("rating", 0),
            "product_id": review.get("product_id"),
            "user_id": review.get("user_id"),
            "created_at": review.get("created_at"),
            "updated_at": review.get("updated_at")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get review error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get review")

@router.put("/reviews/{review_id}")
def update_review(
    review_id: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    rating: Optional[int] = Query(None, ge=1, le=5)
):
    """Update a review"""
    try:
        mongo_db = get_mongo_db()
        if mongo_db is None:
            raise HTTPException(status_code=503, detail="MongoDB unavailable")
        
        from bson import ObjectId
        update_data = {"updated_at": datetime.utcnow()}
        if title: update_data["title"] = title
        if content: update_data["content"] = content
        if rating: update_data["rating"] = rating
        
        result = mongo_db.reviews.update_one(
            {"_id": ObjectId(review_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Review not found")
        
        return {"message": "Review updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update review error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update review")

@router.delete("/reviews/{review_id}")
def delete_review(review_id: str):
    """Delete a review"""
    try:
        mongo_db = get_mongo_db()
        if mongo_db is None:
            raise HTTPException(status_code=503, detail="MongoDB unavailable")
        
        from bson import ObjectId
        result = mongo_db.reviews.delete_one({"_id": ObjectId(review_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Review not found")
        
        return {"message": "Review deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete review error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete review")

# CRUD Operations for Publications (MongoDB)
@router.post("/publications")
def create_publication(
    title: str,
    content: str,
    type: str = "article",
    groups: Optional[List[str]] = None,
    author: Optional[str] = None
):
    """
    📰 CREATE PUBLICATION - Add a new article/blog to MongoDB
    
    This function:
    1. Takes publication information from the user
    2. Creates a new publication document
    3. Saves it to MongoDB
    4. Returns success message with publication ID
    
    Parameters:
        title: Article title (required)
        content: Article content (required)
        type: Type of publication (default: "article")
        groups: Categories/tags (optional)
        author: Author name (optional)
        
    Returns:
        JSON with new publication ID and success message
    """
    try:
        mongo_db = get_mongo_db()
        if mongo_db is None:
            raise HTTPException(status_code=503, detail="MongoDB unavailable")
        
        publication = {
            "title": title,
            "content": content,
            "type": type,
            "groups": groups or [],
            "author": author,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = mongo_db.publications.insert_one(publication)
        return {
            "id": str(result.inserted_id),
            "title": title,
            "type": type,
            "message": "Publication created successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create publication error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create publication")

@router.get("/publications/{publication_id}")
def get_publication(publication_id: str):
    """Get a specific publication by ID"""
    try:
        mongo_db = get_mongo_db()
        if mongo_db is None:
            raise HTTPException(status_code=503, detail="MongoDB unavailable")
        
        from bson import ObjectId
        publication = mongo_db.publications.find_one({"_id": ObjectId(publication_id)})
        if not publication:
            raise HTTPException(status_code=404, detail="Publication not found")
        
        return {
            "id": str(publication["_id"]),
            "title": publication.get("title", ""),
            "content": publication.get("content", ""),
            "type": publication.get("type", "article"),
            "groups": publication.get("groups", []),
            "author": publication.get("author"),
            "created_at": publication.get("created_at"),
            "updated_at": publication.get("updated_at")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get publication error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get publication")

# Bulk Operations
@router.post("/bulk/publications")
def bulk_create_publications(publications: List[Dict[str, Any]]):
    """Bulk create publications in MongoDB"""
    try:
        mongo_db = get_mongo_db()
        if mongo_db is None:
            raise HTTPException(status_code=503, detail="MongoDB unavailable")
        
        publication_docs = []
        for pub_data in publications[:20]:  # Limit to 20 for safety
            publication = {
                "title": pub_data.get("title", "Untitled Article"),
                "content": pub_data.get("content", ""),
                "type": pub_data.get("type", "article"),
                "groups": pub_data.get("groups", []),
                "author": pub_data.get("author"),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            publication_docs.append(publication)
        
        result = mongo_db.publications.insert_many(publication_docs)
        return {
            "message": f"Created {len(result.inserted_ids)} publications successfully",
            "count": len(result.inserted_ids),
            "ids": [str(id) for id in result.inserted_ids]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Bulk create publications error: {e}")
        raise HTTPException(status_code=500, detail="Failed to bulk create publications")

@router.post("/bulk/films")
def bulk_create_films(
    films: List[Dict[str, Any]],
    db: Session = Depends(get_db)
):
    """Bulk create films"""
    try:
        created_films = []
        for film_data in films[:10]:  # Limit to 10 for safety
            film = Film(
                title=film_data.get("title", "Untitled"),
                description=film_data.get("description"),
                release_year=film_data.get("release_year"),
                rental_rate=film_data.get("rental_rate", 4.99),
                length=film_data.get("length"),
                rating=film_data.get("rating", "G"),
                language_id=1
            )
            db.add(film)
            created_films.append(film)
        
        db.commit()
        return {
            "message": f"Created {len(created_films)} films successfully",
            "count": len(created_films)
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Bulk create films error: {e}")
        raise HTTPException(status_code=500, detail="Failed to bulk create films")

@router.post("/bulk/reviews")
def bulk_create_reviews(reviews: List[Dict[str, Any]]):
    """Bulk create reviews in MongoDB"""
    try:
        mongo_db = get_mongo_db()
        if mongo_db is None:
            raise HTTPException(status_code=503, detail="MongoDB unavailable")
        
        review_docs = []
        for review_data in reviews[:20]:  # Limit to 20 for safety
            review = {
                "title": review_data.get("title", "Untitled Review"),
                "content": review_data.get("content", ""),
                "rating": max(1, min(5, review_data.get("rating", 3))),
                "product_id": review_data.get("product_id"),
                "user_id": review_data.get("user_id"),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            review_docs.append(review)
        
        result = mongo_db.reviews.insert_many(review_docs)
        return {
            "message": f"Created {len(result.inserted_ids)} reviews successfully",
            "count": len(result.inserted_ids),
            "ids": [str(id) for id in result.inserted_ids]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Bulk create reviews error: {e}")
        raise HTTPException(status_code=500, detail="Failed to bulk create reviews")