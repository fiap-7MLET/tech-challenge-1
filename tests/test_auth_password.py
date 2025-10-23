"""Tests for password hashing and validation utilities."""

import pytest
from src.services.auth.password import (
    hash_password,
    verify_password,
    validate_password_strength
)


class TestPasswordHashing:
    """Test password hashing functionality."""

    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string."""
        password = "TestPass123"
        hashed = hash_password(password)
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_different_for_same_input(self):
        """Test that hashing same password twice produces different hashes (salt)."""
        password = "TestPass123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 != hash2  # Different due to different salts

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "TestPass123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "TestPass123"
        wrong_password = "WrongPass456"
        hashed = hash_password(password)
        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_case_sensitive(self):
        """Test that password verification is case sensitive."""
        password = "TestPass123"
        hashed = hash_password(password)
        assert verify_password("testpass123", hashed) is False


class TestPasswordStrengthValidation:
    """Test password strength validation."""

    def test_valid_password(self):
        """Test validation of a valid password."""
        is_valid, message = validate_password_strength("ValidPass123")
        assert is_valid is True
        assert message == ""

    def test_password_too_short(self):
        """Test validation fails for password shorter than 8 characters."""
        is_valid, message = validate_password_strength("Short1A")
        assert is_valid is False
        assert "at least 8 characters" in message

    def test_password_no_lowercase(self):
        """Test validation fails for password without lowercase letter."""
        is_valid, message = validate_password_strength("PASSWORD123")
        assert is_valid is False
        assert "lowercase letter" in message

    def test_password_no_uppercase(self):
        """Test validation fails for password without uppercase letter."""
        is_valid, message = validate_password_strength("password123")
        assert is_valid is False
        assert "uppercase letter" in message

    def test_password_no_digit(self):
        """Test validation fails for password without digit."""
        is_valid, message = validate_password_strength("PasswordABC")
        assert is_valid is False
        assert "digit" in message

    def test_password_with_special_characters(self):
        """Test that passwords with special characters are accepted."""
        is_valid, message = validate_password_strength("Pass@word123!")
        assert is_valid is True
        assert message == ""

    def test_minimum_valid_password(self):
        """Test minimum valid password (8 chars, 1 upper, 1 lower, 1 digit)."""
        is_valid, message = validate_password_strength("Passw0rd")
        assert is_valid is True
        assert message == ""
