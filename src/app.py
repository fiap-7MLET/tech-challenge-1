
from fastapi import FastAPI

from src.routes.book_routes import router as book_router
from src.routes.user_routes import router as user_router
from src.routes.health_routes import router as health_router
from src.routes.category_routes import router as category_router

app = FastAPI(title="Tech Challenge API", version="1.0")
app.include_router(book_router)
app.include_router(user_router)
app.include_router(health_router)
app.include_router(category_router)

# Para rodar: poetry run uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

