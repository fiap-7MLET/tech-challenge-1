"""Configuração compartilhada de testes pytest."""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from src.app import app
from src.models import Base
from src.extensions import get_db

# Cria banco de dados de teste compartilhado
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Substitui a dependência do banco de dados para testes."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Sobrescreve a dependência do banco de dados globalmente
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Cria tabelas do banco de dados de teste uma vez para toda a sessão."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_database():
    """Limpa os dados entre cada teste, mantendo a estrutura das tabelas."""
    yield
    # Limpa todas as tabelas após cada teste
    db = TestingSessionLocal()
    try:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
    finally:
        db.close()


@pytest.fixture
def client():
    """Fornece um TestClient para fazer requisições HTTP nos testes."""
    return TestClient(app)


@pytest.fixture
def db():
    """Fornece uma sessão de banco de dados para testes."""
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()
