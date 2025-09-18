from fastapi import FastAPI
from src.api.routes import user, book

app = FastAPI(title="Tech Challenge 1 - FastAPI")

app.include_router(user.router, prefix="/api/v1/users", tags=["Usuários"])
app.include_router(book.router, prefix="/api/v1/books", tags=["Livros"])

"""
Docstring:
Este arquivo inicializa a aplicação FastAPI e inclui as rotas principais.
"""
