import psycopg2
import pymongo
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

def explore_postgres():
    print("EXPLORING POSTGRESQL DATABASE")
    print("=" * 50)
    
    try:
        # Connect to PostgreSQL
        engine = create_engine(os.getenv("DATABASE_URL"))
        
        with engine.connect() as conn:
            # Get all tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result]
            print(f"Found {len(tables)} tables:")
            for table in tables:
                print(f"  • {table}")
            
            print("\n" + "=" * 50)
            
            # Explore key tables with sample data
            key_tables = ['film', 'actor', 'category', 'customer', 'rental', 'payment']
            
            for table in key_tables:
                if table in tables:
                    print(f"\nTABLE: {table.upper()}")
                    print("-" * 30)
                    
                    # Get column info
                    result = conn.execute(text(f"""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns 
                        WHERE table_name = '{table}'
                        ORDER BY ordinal_position;
                    """))
                    
                    columns = list(result)
                    print("Columns:")
                    for col in columns:
                        print(f"  • {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
                    
                    # Get row count
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"Total rows: {count}")
                    
                    # Get sample data
                    if count > 0:
                        result = conn.execute(text(f"SELECT * FROM {table} LIMIT 3"))
                        rows = list(result)
                        print("Sample data:")
                        for i, row in enumerate(rows, 1):
                            print(f"  Row {i}: {dict(zip([col[0] for col in columns], row))}")
                    
                    print()
            
    except Exception as e:
        print(f"❌ PostgreSQL Error: {e}")

def explore_mongodb():
    print("\nEXPLORING MONGODB DATABASE")
    print("=" * 50)
    
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(os.getenv("MONGO_URL"))
        
        # List all databases
        db_names = client.list_database_names()
        print(f"Found databases: {db_names}")
        
        # Explore skillstacker database
        db = client.skillstacker
        collections = db.list_collection_names()
        
        if collections:
            print(f"\nCollections in 'skillstacker' database:")
            for collection in collections:
                print(f"  • {collection}")
                
                # Get sample documents
                coll = db[collection]
                count = coll.count_documents({})
                print(f"    Total documents: {count}")
                
                if count > 0:
                    sample = list(coll.find().limit(2))
                    print(f"    Sample documents:")
                    for i, doc in enumerate(sample, 1):
                        print(f"      Doc {i}: {doc}")
                print()
        else:
            print("No collections found in 'skillstacker' database")
            
            # Check other databases
            for db_name in db_names:
                if db_name not in ['admin', 'local', 'config']:
                    print(f"\nChecking database: {db_name}")
                    other_db = client[db_name]
                    other_collections = other_db.list_collection_names()
                    if other_collections:
                        print(f"  Collections: {other_collections}")
                        for coll_name in other_collections[:3]:  # Check first 3 collections
                            coll = other_db[coll_name]
                            count = coll.count_documents({})
                            print(f"    {coll_name}: {count} documents")
                            if count > 0:
                                sample = coll.find_one()
                                print(f"      Sample: {sample}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ MongoDB Error: {e}")

if __name__ == "__main__":
    explore_postgres()
    explore_mongodb()