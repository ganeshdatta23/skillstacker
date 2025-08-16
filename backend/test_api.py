#!/usr/bin/env python3
import requests
import json

def test_api_endpoints():
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/",
        "/health",
        "/api/v1/products",
        "/api/v1/products/1",
        "/api/v1/reviews/product/1"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"Testing: {url}")
            
            response = requests.get(url, timeout=5)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"  Response: List with {len(data)} items")
                    if data:
                        print(f"  Sample: {json.dumps(data[0], indent=2)[:200]}...")
                else:
                    print(f"  Response: {json.dumps(data, indent=2)[:200]}...")
            else:
                print(f"  Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"  [ERROR] Cannot connect to {url}")
            print("  [INFO] Make sure backend server is running: uvicorn src.main:app --reload")
            break
        except Exception as e:
            print(f"  [ERROR] {e}")
        
        print()

if __name__ == "__main__":
    test_api_endpoints()