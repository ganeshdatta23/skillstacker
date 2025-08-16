#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from sqlalchemy import create_engine, text
from src.core.config import settings
from src.db.models import Film
from src.db.postgres import SessionLocal

def test_database():
    print(f"Database URL: {settings.database_url}")
    
    try:
        # Test connection
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("[OK] Database connection successful")
        
        # Test data
        db = SessionLocal()
        try:
            count = db.query(Film).count()
            print(f"[OK] Found {count} films in database")
            
            if count > 0:
                sample = db.query(Film).first()
                print(f"[OK] Sample film: {sample.title} (ID: {sample.film_id})")
            else:
                print("[WARNING] No films found in database")
                
        finally:
            db.close()
            
    except Exception as e:
        print(f"[ERROR] Database error: {e}")

if __name__ == "__main__":
    test_database()