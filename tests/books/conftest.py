import pytest
from models.books import Book
from extensions import db
from factories import BookFactory

@pytest.fixture
def test_user(app):
    with app.app_context():
        books = BookFactory.create_batch(6)
        db.session.commit()
        yield books
        db.session.query(Book).delete()
        db.session.commit()
