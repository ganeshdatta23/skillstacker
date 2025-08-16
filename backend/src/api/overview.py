from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.dependencies import get_db
from src.db.models import Film, Actor, Category, User, Rental, Payment
from src.db.mongo import get_mongo_client

router = APIRouter()

@router.get("/")
async def get_data_overview(
    db: Session = Depends(get_db)
):
    """Get comprehensive overview of all available data"""
    
    # PostgreSQL data counts
    postgres_data = {
        "films": {
            "total": db.query(Film).count(),
            "sample_titles": [f.title for f in db.query(Film).limit(5).all()]
        },
        "actors": {
            "total": db.query(Actor).count(),
            "sample_names": [f"{a.first_name} {a.last_name}" for a in db.query(Actor).limit(5).all()]
        },
        "categories": {
            "total": db.query(Category).count(),
            "all_categories": [c.name for c in db.query(Category).all()]
        },
        "customers": {
            "total": db.query(User).count(),
            "sample_emails": [u.email for u in db.query(User).limit(5).all() if u.email]
        },
        "rentals": {
            "total": db.query(Rental).count()
        },
        "payments": {
            "total": db.query(Payment).count()
        }
    }
    
    # MongoDB data counts
    try:
        client = await get_mongo_client()
        publications_collection = client["Publications-data"]["Publications"]
        publications_count = await publications_collection.count_documents({})
        
        # Get sample publication titles
        sample_pubs = await publications_collection.find().limit(5).to_list(length=5)
        sample_titles = [pub.get("title", "No title") for pub in sample_pubs]
        
        mongodb_data = {
            "publications": {
                "total": publications_count,
                "sample_titles": sample_titles
            }
        }
    except Exception as e:
        mongodb_data = {
            "publications": {
                "total": 0,
                "error": str(e)
            }
        }
    
    return {
        "postgresql": postgres_data,
        "mongodb": mongodb_data,
        "summary": {
            "total_films": postgres_data["films"]["total"],
            "total_actors": postgres_data["actors"]["total"],
            "total_categories": postgres_data["categories"]["total"],
            "total_customers": postgres_data["customers"]["total"],
            "total_rentals": postgres_data["rentals"]["total"],
            "total_payments": postgres_data["payments"]["total"],
            "total_publications": mongodb_data["publications"]["total"]
        }
    }