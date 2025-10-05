"""Configuração de fixtures do pytest."""

import pytest
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Cria as tabelas do banco de dados antes de executar os testes."""
    from src.extensions import engine
    from src.models import Base
    # Importa os modelos para registrá-los no metadata
    from src.models.book import Book  # noqa: F401
    from src.models.user import User  # noqa: F401

    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)

    yield

    # Limpa as tabelas após os testes
    Base.metadata.drop_all(bind=engine)
