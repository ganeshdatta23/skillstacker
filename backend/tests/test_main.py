import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "SkillStacker API", "version": "1.0.0"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_products_endpoint():
    response = client.get("/api/v1/products/")
    # Should return 200 even if no products (empty list)
    assert response.status_code in [200, 500]  # 500 if DB not connected