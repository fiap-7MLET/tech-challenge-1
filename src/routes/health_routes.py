"""Rotas de health check da API."""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import literal_column, select

from src.extensions import SessionLocal

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
def health():
    """
    Verifica o status da API e a conectividade com o banco de dados.

    Returns:
        JSONResponse: Status da API e do banco de dados
    """
    status_ = "ok"
    db_status = "up"
    error = False
    try:
        db = SessionLocal()
        db.execute(select(literal_column("1")))
        db.close()
    except Exception as e:
        status_ = "error"
        db_status = f"[DB Health Error] {e}"
        error = True
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        if error
        else status.HTTP_200_OK,
        content={"status": status_, "database": db_status},
    )
