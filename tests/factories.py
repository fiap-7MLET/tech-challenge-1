import factory
from models import Book
from extensions import db

class BookFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Book
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    title = factory.Sequence(lambda n: f"Book {n}") # https://factoryboy.readthedocs.io/en/stable/recipes.html#forcing-the-sequence-counter
    price = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    rating = factory.Faker("random_int", min=0, max=5)
    availability = factory.Faker("pybool")
    category = factory.Iterator(["Suspense", "Romance", "Terror"])