"""Rotas para estatísticas e insights sobre os livros (não implementadas)."""

from fastapi import APIRouter, status

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/overview", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def stats_overview():
    """Estatísticas gerais da coleção (não implementado)."""
    return {"message": "Not implemented"}


@router.get("/categories", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def stats_categories():
    """Estatísticas detalhadas por categoria (não implementado)."""
    return {"message": "Not implemented"}
