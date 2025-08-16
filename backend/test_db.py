from src.api.postgres import engine, SessionLocal
from src.db.models import User, Product, Order, Payment

def test_connection():
    try:
        # Test engine connection
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("SELECT 1"))
            print("[OK] Database connection successful")
        
        # Test session
        db = SessionLocal()
        try:
            # Test basic queries
            user_count = db.query(User).count()
            print(f"[OK] Users table accessible - {user_count} records")
            
            product_count = db.query(Product).count()
            print(f"[OK] Products table accessible - {product_count} records")
            
            order_count = db.query(Order).count()
            print(f"[OK] Orders table accessible - {order_count} records")
            
        except Exception as e:
            print(f"[ERROR] Query error: {e}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")

if __name__ == "__main__":
    test_connection()