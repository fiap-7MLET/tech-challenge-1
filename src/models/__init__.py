"""Modelos de dados compartilhados."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Importa os modelos para garantir que estejam registrados com Base
from src.models.book import Book
from src.models.user import User
from src.models.scraping_job import ScrapingJob

__all__ = ["Base", "Book", "User", "ScrapingJob"]
