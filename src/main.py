from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Request
from src.api.routes import user, book, scraping
from alembic import command
from alembic.config import Config
from pathlib import Path
from contextlib import asynccontextmanager


import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação FastAPI.
    Executa as migrações do banco de dados usando Alembic no startup.
    Adiciona logs e tratamento de exceções para garantir robustez.
    """
    try:
        alembic_cfg = Config(str(Path(__file__).parent.parent / "alembic.ini"))
        command.upgrade(alembic_cfg, "head")
        logging.info("Migrações Alembic executadas com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao executar migrações Alembic: {e}")
        raise
    yield

app = FastAPI(title="Tech Challenge 1 - FastAPI", lifespan=lifespan)

app.include_router(user.router, prefix="/api/v1/users", tags=["Usuários"])
app.include_router(book.router, prefix="/api/v1/books", tags=["Livros"])
app.include_router(scraping.router, prefix="/api/v1/scraping", tags=["Scraping"])

"""
Docstring:
Este arquivo inicializa a aplicação FastAPI e inclui as rotas principais.
"""
