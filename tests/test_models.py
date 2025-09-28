import pytest
from src.models.book import Book
from src.models.user import User

def test_book_model_fields():
    fields = ["id", "title", "price", "rating", "availability", "category", "image"]
    for field in fields:
        assert hasattr(Book, field)

def test_user_model_fields():
    fields = ["id", "email", "password"]
    for field in fields:
        assert hasattr(User, field)
