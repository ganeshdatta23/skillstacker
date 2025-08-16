from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.dependencies import get_db
from src.db.models import Actor
from src.schemas import ActorResponse

router = APIRouter()

@router.get("/", response_model=List[ActorResponse])
def get_actors(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=10000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Actor)
    
    if search:
        query = query.filter(
            (Actor.first_name.ilike(f"%{search}%")) |
            (Actor.last_name.ilike(f"%{search}%"))
        )
    
    return query.offset(skip).limit(limit).all()

@router.get("/all", response_model=List[ActorResponse])
def get_all_actors(db: Session = Depends(get_db)):
    return db.query(Actor).all()

@router.get("/stats")
def get_actor_stats(db: Session = Depends(get_db)):
    total_actors = db.query(Actor).count()
    return {"total_actors": total_actors}

@router.get("/{actor_id}", response_model=ActorResponse)
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(Actor).filter(Actor.actor_id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor