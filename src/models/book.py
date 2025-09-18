
from sqlalchemy import Column, Integer, String, Numeric, Boolean
from src.extensions import Base

class Book(Base):
    """
    Modelo de livro para persistência no banco de dados.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), unique=True, nullable=False, index=True)
    price = Column(Numeric(8,2), nullable=False)
    rating = Column(Integer, nullable=False)
    availability = Column(Boolean, nullable=False, default=True)
    category = Column(String(120), nullable=False)
    image = Column(String(120), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": float(self.price),
            "rating": self.rating,
            "availability": self.availability,
            "category": self.category,
            "image": self.image
        }
