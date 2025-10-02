"""Schemas Pydantic para validação de dados da API."""

from pydantic import BaseModel, ConfigDict
from typing import Optional

class BookSchema(BaseModel):
    """
    Schema para representação de um livro na API.

    Attributes:
        id: Identificador único do livro
        title: Título do livro
        price: Preço do livro
        rating: Avaliação do livro (1-5)
        availability: Indica se o livro está disponível
        category: Categoria do livro
        image: URL da imagem do livro
    """
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    title: str
    price: float
    rating: int
    availability: bool
    category: str
    image: Optional[str] = None

class UserSchema(BaseModel):
    """Schema para representação de um usuário na API."""
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    email: str
    password: str
