from fastapi import FastAPI
from src.api.routes import user, book, scraping
from alembic import command
from alembic.config import Config
from pathlib import Path

app = FastAPI(title="Tech Challenge 1 - FastAPI")

@app.on_event("startup")
def startup_event():
    """
    Evento de inicialização da aplicação.
    Executa as migrações do banco de dados usando Alembic.
    """
    alembic_cfg = Config(str(Path(__file__).parent.parent / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

app.include_router(user.router, prefix="/api/v1/users", tags=["Usuários"])
app.include_router(book.router, prefix="/api/v1/books", tags=["Livros"])
app.include_router(scraping.router, prefix="/api/v1/scraping", tags=["Scraping"])

"""
Docstring:
Este arquivo inicializa a aplicação FastAPI e inclui as rotas principais.
"""
