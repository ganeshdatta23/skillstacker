#!/usr/bin/env python3
"""
Test script for CRUD operations in the unified data API
Run this after starting the FastAPI server to test all CRUD endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/unified"

def test_film_crud():
    """Test Film CRUD operations"""
    print("=== Testing Film CRUD Operations ===")
    
    # CREATE
    print("1. Creating a new film...")
    film_data = {
        "title": "Test Movie",
        "description": "A test movie for CRUD operations",
        "release_year": 2024,
        "rental_rate": 5.99,
        "length": 120,
        "rating": "PG-13"
    }
    
    response = requests.post(f"{BASE_URL}/films", params=film_data)
    if response.status_code == 200:
        film_id = response.json()["id"]
        print(f"✓ Film created with ID: {film_id}")
        
        # READ
        print("2. Reading the created film...")
        response = requests.get(f"{BASE_URL}/films/{film_id}")
        if response.status_code == 200:
            print(f"✓ Film retrieved: {response.json()['title']}")
            
            # UPDATE
            print("3. Updating the film...")
            update_data = {"title": "Updated Test Movie", "rating": "R"}
            response = requests.put(f"{BASE_URL}/films/{film_id}", params=update_data)
            if response.status_code == 200:
                print("✓ Film updated successfully")
                
                # DELETE
                print("4. Deleting the film...")
                response = requests.delete(f"{BASE_URL}/films/{film_id}")
                if response.status_code == 200:
                    print("✓ Film deleted successfully")
                else:
                    print(f"✗ Delete failed: {response.text}")
            else:
                print(f"✗ Update failed: {response.text}")
        else:
            print(f"✗ Read failed: {response.text}")
    else:
        print(f"✗ Create failed: {response.text}")

def test_actor_crud():
    """Test Actor CRUD operations"""
    print("\n=== Testing Actor CRUD Operations ===")
    
    # CREATE
    print("1. Creating a new actor...")
    actor_data = {
        "first_name": "John",
        "last_name": "TestActor"
    }
    
    response = requests.post(f"{BASE_URL}/actors", params=actor_data)
    if response.status_code == 200:
        actor_id = response.json()["id"]
        print(f"✓ Actor created with ID: {actor_id}")
        
        # READ
        print("2. Reading the created actor...")
        response = requests.get(f"{BASE_URL}/actors/{actor_id}")
        if response.status_code == 200:
            print(f"✓ Actor retrieved: {response.json()['full_name']}")
            
            # UPDATE
            print("3. Updating the actor...")
            update_data = {"first_name": "Jane", "last_name": "UpdatedActor"}
            response = requests.put(f"{BASE_URL}/actors/{actor_id}", params=update_data)
            if response.status_code == 200:
                print("✓ Actor updated successfully")
                
                # DELETE
                print("4. Deleting the actor...")
                response = requests.delete(f"{BASE_URL}/actors/{actor_id}")
                if response.status_code == 200:
                    print("✓ Actor deleted successfully")
                else:
                    print(f"✗ Delete failed: {response.text}")
            else:
                print(f"✗ Update failed: {response.text}")
        else:
            print(f"✗ Read failed: {response.text}")
    else:
        print(f"✗ Create failed: {response.text}")

def test_review_crud():
    """Test Review CRUD operations (MongoDB)"""
    print("\n=== Testing Review CRUD Operations (MongoDB) ===")
    
    # CREATE
    print("1. Creating a new review...")
    review_data = {
        "title": "Great Product!",
        "content": "This is a test review for CRUD operations. The product is amazing!",
        "rating": 5,
        "product_id": 1,
        "user_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/reviews", params=review_data)
    if response.status_code == 200:
        review_id = response.json()["id"]
        print(f"✓ Review created with ID: {review_id}")
        
        # READ
        print("2. Reading the created review...")
        response = requests.get(f"{BASE_URL}/reviews/{review_id}")
        if response.status_code == 200:
            print(f"✓ Review retrieved: {response.json()['title']}")
            
            # UPDATE
            print("3. Updating the review...")
            update_data = {"title": "Updated Review", "rating": 4}
            response = requests.put(f"{BASE_URL}/reviews/{review_id}", params=update_data)
            if response.status_code == 200:
                print("✓ Review updated successfully")
                
                # DELETE
                print("4. Deleting the review...")
                response = requests.delete(f"{BASE_URL}/reviews/{review_id}")
                if response.status_code == 200:
                    print("✓ Review deleted successfully")
                else:
                    print(f"✗ Delete failed: {response.text}")
            else:
                print(f"✗ Update failed: {response.text}")
        else:
            print(f"✗ Read failed: {response.text}")
    else:
        print(f"✗ Create failed: {response.text}")

def test_bulk_operations():
    """Test bulk operations"""
    print("\n=== Testing Bulk Operations ===")
    
    # Bulk create films
    print("1. Bulk creating films...")
    films_data = [
        {"title": "Bulk Film 1", "description": "First bulk film", "rating": "G"},
        {"title": "Bulk Film 2", "description": "Second bulk film", "rating": "PG"},
        {"title": "Bulk Film 3", "description": "Third bulk film", "rating": "PG-13"}
    ]
    
    response = requests.post(f"{BASE_URL}/bulk/films", json=films_data)
    if response.status_code == 200:
        print(f"✓ Bulk films created: {response.json()['count']} films")
    else:
        print(f"✗ Bulk films failed: {response.text}")
    
    # Bulk create reviews
    print("2. Bulk creating reviews...")
    reviews_data = [
        {"title": "Bulk Review 1", "content": "First bulk review", "rating": 5},
        {"title": "Bulk Review 2", "content": "Second bulk review", "rating": 4},
        {"title": "Bulk Review 3", "content": "Third bulk review", "rating": 3}
    ]
    
    response = requests.post(f"{BASE_URL}/bulk/reviews", json=reviews_data)
    if response.status_code == 200:
        print(f"✓ Bulk reviews created: {response.json()['count']} reviews")
    else:
        print(f"✗ Bulk reviews failed: {response.text}")

def test_search_and_stats():
    """Test search and statistics endpoints"""
    print("\n=== Testing Search and Statistics ===")
    
    # Search
    print("1. Testing unified search...")
    response = requests.get(f"{BASE_URL}/search", params={"q": "test", "limit": 5})
    if response.status_code == 200:
        results = response.json()
        print(f"✓ Search completed. Total results: {results['total_results']}")
    else:
        print(f"✗ Search failed: {response.text}")
    
    # Statistics
    print("2. Getting statistics...")
    response = requests.get(f"{BASE_URL}/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"✓ Statistics retrieved. Total records: {stats['total']}")
    else:
        print(f"✗ Statistics failed: {response.text}")
    
    # Categories
    print("3. Getting categories...")
    response = requests.get(f"{BASE_URL}/categories")
    if response.status_code == 200:
        categories = response.json()
        print(f"✓ Categories retrieved: {len(categories)} category types")
    else:
        print(f"✗ Categories failed: {response.text}")

def main():
    """Run all CRUD tests"""
    print("Starting CRUD Operations Test Suite")
    print("=" * 50)
    
    try:
        # Test basic connectivity
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code != 200:
            print("✗ Cannot connect to API. Make sure the server is running on localhost:8000")
            return
        
        # Run all tests
        test_film_crud()
        test_actor_crud()
        test_review_crud()
        test_bulk_operations()
        test_search_and_stats()
        
        print("\n" + "=" * 50)
        print("✓ All CRUD operations test completed!")
        
    except requests.exceptions.ConnectionError:
        print("✗ Connection error. Make sure the FastAPI server is running on localhost:8000")
    except Exception as e:
        print(f"✗ Test failed with error: {e}")

if __name__ == "__main__":
    main()