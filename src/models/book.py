"""Modelo de dados para livros."""

from sqlalchemy import Column, Integer, String, Numeric, Boolean
from src.models import Base

class Book(Base):
    """
    Modelo representando um livro no banco de dados.

    Attributes:
        id: Identificador único do livro
        title: Título do livro (único)
        price: Preço do livro
        rating: Avaliação do livro (1-5)
        availability: Indica se o livro está disponível em estoque
        category: Categoria do livro
        image: URL da imagem do livro
    """
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(120), unique=True, nullable=False)
    price = Column(Numeric(8,2), nullable=False)
    rating = Column(Integer, nullable=False)
    availability = Column(Boolean, nullable=False, default=True)
    category = Column(String(120), nullable=False)
    image = Column(String(120), nullable=True)
