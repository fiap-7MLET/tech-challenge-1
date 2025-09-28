
from sqlalchemy import Column, Integer, String, Numeric, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(120), unique=True, nullable=False)
    price = Column(Numeric(8,2), nullable=False)
    rating = Column(Integer, nullable=False)
    availability = Column(Boolean, nullable=False, default=True)
    category = Column(String(120), nullable=False)
    image = Column(String(120), nullable=True)
