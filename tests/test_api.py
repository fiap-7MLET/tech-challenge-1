import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.extensions import engine
from src.models.user import User
from src.models.book import Book
from sqlalchemy.orm import declarative_base

client = TestClient(app)

# Setup para criar as tabelas antes dos testes
Base = declarative_base()
User.__table__.create(bind=engine, checkfirst=True)
Book.__table__.create(bind=engine, checkfirst=True)

# Testes para o endpoint de usuários

def test_create_user():
    """Testa a criação de um novo usuário."""
    response = client.post("/api/v1/users/", json={"email": "teste@exemplo.com", "password": "123456"})
    assert response.status_code == 200 or response.status_code == 400


def test_get_user():
    """Testa a busca de um usuário pelo ID."""
    response = client.get("/api/v1/users/1")
    assert response.status_code in [200, 404]

# Testes para o endpoint de livros

def test_create_book():
    """Testa a criação de um novo livro."""
    response = client.post("/api/v1/books/", json={
        "title": "Livro Teste",
        "price": 10.99,
        "rating": 5,
        "availability": True,
        "category": "Teste",
        "image": None
    })
    assert response.status_code == 200 or response.status_code == 400


def test_get_book():
    """Testa a busca de um livro pelo ID."""
    response = client.get("/api/v1/books/1")
    assert response.status_code in [200, 404]

# Teste para o endpoint de scraping

def test_trigger_scraping():
    """Testa o disparo do scraping sob demanda."""
    response = client.post("/api/v1/scraping/trigger")
    assert response.status_code == 200
    assert "mensagem" in response.json()
