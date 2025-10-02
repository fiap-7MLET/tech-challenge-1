"""Aplicação principal FastAPI para consulta de livros."""

from fastapi import FastAPI

from src.routes.book_routes import router as book_router
from src.routes.user_routes import router as user_router
from src.routes.health_routes import router as health_router
from src.routes.category_routes import router as category_router
from src.routes.scraping_routes import router as scraping_router
from src.routes.stats_routes import router as stats_router
from src.routes.ml_routes import router as ml_router

app = FastAPI(
    title="Tech Challenge API",
    version="1.0",
    description="API pública para consulta de livros extraídos via web scraping"
)

# Registra todos os roteadores
app.include_router(book_router)
app.include_router(user_router)
app.include_router(health_router)
app.include_router(category_router)
app.include_router(scraping_router)
app.include_router(stats_router)
app.include_router(ml_router)

# Para rodar: uv run uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

