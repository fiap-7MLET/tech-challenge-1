"""Modelo de dados para usuários."""

from sqlalchemy import Column, Integer, String
from src.models import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
