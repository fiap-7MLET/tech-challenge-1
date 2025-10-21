import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_health_route():
    response = client.get("/health/")
    assert response.status_code in [200, 500]
    assert "status" in response.json()
    assert "database" in response.json()

def test_books_route():
    response = client.get("/books/")
    assert response.status_code == 200
    assert "data" in response.json()
    assert "page" in response.json()
    assert "per_page" in response.json()
    assert "total" in response.json()
    assert "pages" in response.json()
    assert "next" in response.json()
    assert "previous" in response.json()

def test_categories_route():
    response = client.get("/categories/")
    assert response.status_code == 200
    assert "data" in response.json()
    assert "page" in response.json()
    assert "per_page" in response.json()
    assert "total" in response.json()
    assert "pages" in response.json()
    assert "next" in response.json()
    assert "previous" in response.json()

def test_auth_routes():
    for endpoint in ["/auth/register", "/auth/login", "/auth/logout", "/auth/refresh"]:
        response = client.post(endpoint)
        assert response.status_code == 501
