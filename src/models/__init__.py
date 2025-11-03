"""Modelos de dados compartilhados."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Importa os modelos para garantir que estejam registrados com Base
from src.models.book import Book  # noqa: E402
from src.models.scraping_job import ScrapingJob  # noqa: E402
from src.models.user import User  # noqa: E402

__all__ = ["Base", "Book", "User", "ScrapingJob"]
