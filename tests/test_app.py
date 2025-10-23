import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_health_route():
    response = client.get("/health/")
    assert response.status_code in [200, 500]
    assert "status" in response.json()
    assert "database" in response.json()

def test_books_route_requires_auth():
    """Test that books route requires authentication."""
    response = client.get("/books/")
    assert response.status_code == 401

def test_categories_route_requires_auth():
    """Test that categories route requires authentication."""
    response = client.get("/categories/")
    assert response.status_code == 401

def test_auth_register_route_exists():
    """Test that auth register endpoint exists (returns 422 for empty body)."""
    response = client.post("/api/v1/auth/register")
    assert response.status_code == 422  # Validation error for missing body

def test_auth_login_route_exists():
    """Test that auth login endpoint exists (returns 422 for empty body)."""
    response = client.post("/api/v1/auth/login")
    assert response.status_code == 422  # Validation error for missing body
