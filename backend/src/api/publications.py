from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
import pymongo
from src.db.mongo import get_mongo_client

router = APIRouter()

@router.get("/")
async def get_publications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None, description="Search in title"),
    type_filter: Optional[str] = Query(None, description="Filter by type (Journal, etc.)"),
    group: Optional[str] = Query(None, description="Filter by group")
):
    """Get publications from MongoDB - 364,908 research publications available"""
    
    try:
        # Build query
        query = {}
        
        if search:
            query["title"] = {"$regex": search, "$options": "i"}
        
        if type_filter:
            query["type"] = type_filter
        
        if group:
            query["groups"] = {"$in": [group]}
        
        # Get publications collection
        client = await get_mongo_client()
        collection = client["Publications-data"]["Publications"]
        
        # Get total count
        total = await collection.count_documents(query)
        
        # Get paginated results
        cursor = collection.find(query).skip(skip).limit(limit)
        publications = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string for JSON serialization
        for pub in publications:
            pub["_id"] = str(pub["_id"])
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "publications": publications
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching publications: {str(e)}")

@router.get("/stats")
async def get_publication_stats():
    """Get comprehensive publication statistics"""
    
    try:
        client = await get_mongo_client()
        collection = client["Publications-data"]["Publications"]
        
        # Total count
        total = await collection.count_documents({})
        
        return {
            "total_publications": total
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

@router.get("/search")
async def search_publications(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100)
):
    """Advanced search in publications"""
    
    try:
        client = await get_mongo_client()
        collection = client["Publications-data"]["Publications"]
        
        # Text search query
        query = {
            "$or": [
                {"title": {"$regex": q, "$options": "i"}},
                {"related_title": {"$regex": q, "$options": "i"}},
                {"groups": {"$in": [{"$regex": q, "$options": "i"}]}},
                {"subgroups": {"$in": [{"$regex": q, "$options": "i"}]}}
            ]
        }
        
        cursor = collection.find(query).limit(limit)
        results = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for result in results:
            result["_id"] = str(result["_id"])
        
        return {
            "query": q,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching publications: {str(e)}")