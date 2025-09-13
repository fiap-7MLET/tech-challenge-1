import pytest
from models.book import Book
from extensions import db
from tests.factories import BookFactory

@pytest.fixture
def seed_books(app, db):
    with app.app_context():
        BookFactory.reset_sequence(0)
        books = BookFactory.create_batch(6)
        db.session.commit()
        yield books
        db.session.query(Book).delete()
        db.session.commit()
