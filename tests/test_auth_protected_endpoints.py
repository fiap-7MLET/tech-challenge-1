"""Tests for protected endpoints requiring authentication."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app import app
from src.extensions import get_db
from src.models import Base


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_protected.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create and cleanup test database for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def regular_user_token():
    """Create a regular user and return their access token."""
    # First user is admin, so create second user
    client.post(
        "/api/v1/auth/register",
        json={"email": "admin@example.com", "password": "AdminPass123"}
    )
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "UserPass123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def admin_user_token():
    """Create an admin user (first user) and return their access token."""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "admin@example.com", "password": "AdminPass123"}
    )
    return response.json()["access_token"]


class TestProtectedBooksEndpoints:
    """Test that books endpoints require authentication."""

    def test_books_list_without_auth(self):
        """Test that books list endpoint requires authentication."""
        response = client.get("/books/")
        assert response.status_code == 401

    def test_books_list_with_auth(self, regular_user_token):
        """Test that books list endpoint works with authentication."""
        response = client.get(
            "/books/",
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        assert response.status_code == 200

    def test_books_search_without_auth(self):
        """Test that books search endpoint requires authentication."""
        response = client.get("/books/search?title=test")
        assert response.status_code == 401

    def test_books_search_with_auth(self, regular_user_token):
        """Test that books search endpoint works with authentication."""
        response = client.get(
            "/books/search?title=test",
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        assert response.status_code == 200

    def test_books_by_id_without_auth(self):
        """Test that books by ID endpoint requires authentication."""
        response = client.get("/books/1")
        assert response.status_code == 401

    def test_books_by_id_with_auth(self, regular_user_token):
        """Test that books by ID endpoint works with authentication."""
        response = client.get(
            "/books/999",  # Non-existent book
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        # Should return 404 (not found) not 401 (unauthorized)
        assert response.status_code == 404


class TestProtectedCategoriesEndpoints:
    """Test that categories endpoints require authentication."""

    def test_categories_list_without_auth(self):
        """Test that categories list endpoint requires authentication."""
        response = client.get("/categories/")
        assert response.status_code == 401

    def test_categories_list_with_auth(self, regular_user_token):
        """Test that categories list endpoint works with authentication."""
        response = client.get(
            "/categories/",
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        assert response.status_code == 200


class TestProtectedScrapingEndpoints:
    """Test that scraping endpoints require authentication."""

    def test_scraping_status_without_auth(self):
        """Test that scraping status endpoint requires authentication."""
        response = client.get("/scraping/status")
        assert response.status_code == 401

    def test_scraping_status_with_auth(self, regular_user_token):
        """Test that scraping status endpoint works with authentication."""
        response = client.get(
            "/scraping/status",
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        assert response.status_code == 200

    def test_scraping_trigger_without_auth(self):
        """Test that scraping trigger endpoint requires authentication."""
        response = client.post("/scraping/trigger")
        assert response.status_code == 401

    def test_scraping_trigger_regular_user(self, regular_user_token):
        """Test that scraping trigger requires admin privileges."""
        response = client.post(
            "/scraping/trigger",
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        assert response.status_code == 403  # Forbidden (not admin)
        assert "admin" in response.json()["detail"].lower()

    def test_scraping_trigger_admin_user(self, admin_user_token):
        """Test that scraping trigger works for admin users."""
        response = client.post(
            "/scraping/trigger",
            headers={"Authorization": f"Bearer {admin_user_token}"}
        )
        # Should not return 401 or 403 (authentication/authorization errors)
        assert response.status_code != 401
        assert response.status_code != 403


class TestProtectedStatsEndpoints:
    """Test that stats endpoints require authentication."""

    def test_stats_overview_without_auth(self):
        """Test that stats overview endpoint requires authentication."""
        response = client.get("/stats/overview")
        assert response.status_code == 401

    def test_stats_overview_with_auth(self, regular_user_token):
        """Test that stats overview endpoint works with authentication."""
        response = client.get(
            "/stats/overview",
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        # 501 = Not Implemented (the endpoint itself is not implemented)
        # But it should not return 401 (unauthorized)
        assert response.status_code == 501

    def test_stats_categories_without_auth(self):
        """Test that stats categories endpoint requires authentication."""
        response = client.get("/stats/categories")
        assert response.status_code == 401

    def test_stats_categories_with_auth(self, regular_user_token):
        """Test that stats categories endpoint works with authentication."""
        response = client.get(
            "/stats/categories",
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        assert response.status_code == 501


class TestProtectedMLEndpoints:
    """Test that ML endpoints require authentication."""

    def test_ml_features_without_auth(self):
        """Test that ML features endpoint requires authentication."""
        response = client.get("/ml/features")
        assert response.status_code == 401

    def test_ml_features_with_auth(self, regular_user_token):
        """Test that ML features endpoint works with authentication."""
        response = client.get(
            "/ml/features",
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        assert response.status_code == 501

    def test_ml_training_data_without_auth(self):
        """Test that ML training data endpoint requires authentication."""
        response = client.get("/ml/training-data")
        assert response.status_code == 401

    def test_ml_predictions_without_auth(self):
        """Test that ML predictions endpoint requires authentication."""
        response = client.post("/ml/predictions")
        assert response.status_code == 401


class TestHealthEndpointNoAuth:
    """Test that health endpoint does NOT require authentication."""

    def test_health_endpoint_public(self):
        """Test that health endpoint is publicly accessible."""
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestInvalidTokens:
    """Test behavior with invalid tokens."""

    def test_malformed_token(self):
        """Test that malformed token is rejected."""
        response = client.get(
            "/books/",
            headers={"Authorization": "Bearer malformed-token"}
        )
        assert response.status_code == 401

    def test_expired_token(self):
        """Test that expired token is rejected."""
        # This would require mocking time or using a very short expiry
        # For now, we just test with an obviously invalid token
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0In0.invalid"
        response = client.get(
            "/books/",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401

    def test_missing_bearer_prefix(self):
        """Test that token without 'Bearer' prefix is rejected."""
        response = client.get(
            "/books/",
            headers={"Authorization": "some-token"}
        )
        assert response.status_code == 401
