#!/usr/bin/env python3
"""Initialize database with sample data"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from src.db.postgres import engine, SessionLocal
from src.db.models import Base, User, Product
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_database():
    """Initialize database with tables and sample data"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already initialized")
            return
        
        # Create sample users
        users = [
            User(
                email="demo@skillstacker.com",
                full_name="Demo User",
                password_hash=pwd_context.hash("demo123"),
                is_active=True,
                is_admin=False
            ),
            User(
                email="admin@skillstacker.com", 
                full_name="Admin User",
                password_hash=pwd_context.hash("admin123"),
                is_active=True,
                is_admin=True
            )
        ]
        
        for user in users:
            db.add(user)
        
        # Create sample products
        products = [
            Product(
                name="Wireless Bluetooth Headphones",
                description="High-quality wireless headphones with noise cancellation and 30-hour battery life.",
                price=199.99,
                category="Electronics",
                rating=4.5,
                reviews_count=128
            ),
            Product(
                name="Smart Fitness Watch",
                description="Advanced fitness tracker with heart rate monitoring, GPS, and smartphone integration.",
                price=299.99,
                category="Electronics", 
                rating=4.3,
                reviews_count=89
            ),
            Product(
                name="Organic Coffee Beans",
                description="Premium organic coffee beans sourced from sustainable farms in Colombia.",
                price=24.99,
                category="Food & Beverage",
                rating=4.7,
                reviews_count=245
            ),
            Product(
                name="Yoga Mat Premium",
                description="Non-slip yoga mat made from eco-friendly materials, perfect for all types of yoga.",
                price=49.99,
                category="Sports & Fitness",
                rating=4.4,
                reviews_count=156
            )
        ]
        
        for product in products:
            db.add(product)
        
        db.commit()
        print("Database initialized successfully!")
        print("Demo Accounts:")
        print("User: demo@skillstacker.com / demo123")
        print("Admin: admin@skillstacker.com / admin123")
        print(f"Created {len(products)} sample products")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()