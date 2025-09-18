
from sqlalchemy import Column, Integer, String
from src.extensions import Base

class User(Base):
    """
    Modelo de usuário para persistência no banco de dados.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)
