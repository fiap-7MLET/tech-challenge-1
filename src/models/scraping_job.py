"""Modelo de dados para jobs de scraping."""

from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timezone
from src.models import Base


class ScrapingJob(Base):
    """
    Modelo representando um job de scraping no banco de dados.

    Attributes:
        id: Identificador único do job
        status: Status do job (pending, in_progress, completed, error)
        started_at: Timestamp de início do job
        completed_at: Timestamp de conclusão do job
        books_scraped: Número de livros coletados
        books_saved: Número de livros salvos no banco
        error_message: Mensagem de erro se o job falhou
        csv_file: Caminho do arquivo CSV gerado
    """
    __tablename__ = "scraping_jobs"

    id = Column(Integer, primary_key=True)
    status = Column(String(20), nullable=False, default="pending")  # pending, in_progress, completed, error
    started_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    books_scraped = Column(Integer, nullable=True)
    books_saved = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    csv_file = Column(String(255), nullable=True)
