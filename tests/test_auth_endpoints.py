"""Tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app import app
from src.extensions import get_db
from src.models import Base
from src.models.user import User


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"
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


class TestUserRegistration:
    """Test user registration endpoint."""

    def test_register_first_user_is_admin(self):
        """Test that first registered user becomes admin."""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "admin@example.com", "password": "AdminPass123"}
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

        # Verify user is admin
        token = data["access_token"]
        me_response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        user_data = me_response.json()
        assert user_data["is_admin"] is True

    def test_register_second_user_not_admin(self):
        """Test that second registered user is not admin."""
        # Register first user (admin)
        client.post(
            "/api/v1/auth/register",
            json={"email": "admin@example.com", "password": "AdminPass123"}
        )

        # Register second user
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "user@example.com", "password": "UserPass123"}
        )
        assert response.status_code == 201
        data = response.json()

        # Verify user is not admin
        token = data["access_token"]
        me_response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        user_data = me_response.json()
        assert user_data["is_admin"] is False

    def test_register_duplicate_email(self):
        """Test registration with duplicate email fails."""
        email = "test@example.com"
        password = "TestPass123"

        # First registration
        response1 = client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": password}
        )
        assert response1.status_code == 201

        # Second registration with same email
        response2 = client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": password}
        )
        assert response2.status_code == 400
        assert "already registered" in response2.json()["detail"].lower()

    def test_register_weak_password(self):
        """Test registration with weak password fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "password": "weak"}
        )
        # 422 = Pydantic validation error for min_length
        assert response.status_code == 422

    def test_register_invalid_email(self):
        """Test registration with invalid email fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "not-an-email", "password": "TestPass123"}
        )
        assert response.status_code == 422  # Validation error


class TestUserLogin:
    """Test user login endpoint."""

    def test_login_success(self):
        """Test successful login."""
        email = "test@example.com"
        password = "TestPass123"

        # Register user first
        client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": password}
        )

        # Login
        response = client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": password}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self):
        """Test login with wrong password fails."""
        email = "test@example.com"
        password = "TestPass123"

        # Register user
        client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": password}
        )

        # Login with wrong password
        response = client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": "WrongPass123"}
        )
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self):
        """Test login with nonexistent user fails."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "nonexistent@example.com", "password": "TestPass123"}
        )
        assert response.status_code == 401


class TestTokenRefresh:
    """Test token refresh endpoint."""

    def test_refresh_token_success(self):
        """Test successful token refresh."""
        # Register and get tokens
        register_response = client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "password": "TestPass123"}
        )
        refresh_token = register_response.json()["refresh_token"]

        # Refresh token
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_refresh_with_invalid_token(self):
        """Test refresh with invalid token fails."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid.token.here"}
        )
        assert response.status_code == 401

    def test_refresh_with_access_token(self):
        """Test refresh with access token (not refresh token) fails."""
        # Register and get tokens
        register_response = client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "password": "TestPass123"}
        )
        access_token = register_response.json()["access_token"]

        # Try to refresh with access token
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": access_token}
        )
        assert response.status_code == 401
        assert "token type" in response.json()["detail"].lower()


class TestGetCurrentUser:
    """Test get current user endpoint."""

    def test_get_current_user_success(self):
        """Test getting current user info."""
        email = "test@example.com"

        # Register
        register_response = client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "TestPass123"}
        )
        token = register_response.json()["access_token"]

        # Get current user
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == email
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data

    def test_get_current_user_no_token(self):
        """Test getting current user without token fails."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token fails."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401
