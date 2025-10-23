"""Tests for JWT token management."""

import pytest
from datetime import timedelta
from src.services.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token_type
)


class TestJWTTokenCreation:
    """Test JWT token creation."""

    def test_create_access_token(self):
        """Test creating an access token."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token(self):
        """Test creating a refresh token."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_refresh_token(data)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_custom_expiry(self):
        """Test creating access token with custom expiration."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data, expires_delta=timedelta(minutes=30))
        assert isinstance(token, str)

    def test_create_refresh_token_with_custom_expiry(self):
        """Test creating refresh token with custom expiration."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_refresh_token(data, expires_delta=timedelta(days=7))
        assert isinstance(token, str)


class TestJWTTokenDecoding:
    """Test JWT token decoding."""

    def test_decode_valid_access_token(self):
        """Test decoding a valid access token."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)
        payload = decode_token(token)

        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == 1
        assert payload["type"] == "access"

    def test_decode_valid_refresh_token(self):
        """Test decoding a valid refresh token."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_refresh_token(data)
        payload = decode_token(token)

        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == 1
        assert payload["type"] == "refresh"

    def test_decode_invalid_token(self):
        """Test decoding an invalid token."""
        invalid_token = "invalid.token.here"
        payload = decode_token(invalid_token)
        assert payload is None

    def test_decode_malformed_token(self):
        """Test decoding a malformed token."""
        malformed_token = "not-a-jwt-token"
        payload = decode_token(malformed_token)
        assert payload is None


class TestTokenTypeVerification:
    """Test token type verification."""

    def test_verify_access_token_type(self):
        """Test verifying access token type."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)
        payload = decode_token(token)

        assert verify_token_type(payload, "access") is True
        assert verify_token_type(payload, "refresh") is False

    def test_verify_refresh_token_type(self):
        """Test verifying refresh token type."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_refresh_token(data)
        payload = decode_token(token)

        assert verify_token_type(payload, "refresh") is True
        assert verify_token_type(payload, "access") is False

    def test_verify_token_type_missing_type(self):
        """Test verifying token without type field."""
        payload = {"sub": "test@example.com", "user_id": 1}
        assert verify_token_type(payload, "access") is False


class TestTokenDataIntegrity:
    """Test token data integrity."""

    def test_token_preserves_data(self):
        """Test that token preserves all data fields."""
        data = {
            "sub": "test@example.com",
            "user_id": 42,
            "custom_field": "custom_value"
        }
        token = create_access_token(data)
        payload = decode_token(token)

        assert payload["sub"] == data["sub"]
        assert payload["user_id"] == data["user_id"]
        assert payload["custom_field"] == data["custom_field"]

    def test_token_contains_expiration(self):
        """Test that token contains expiration field."""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)
        payload = decode_token(token)

        assert "exp" in payload
        assert isinstance(payload["exp"], int)
