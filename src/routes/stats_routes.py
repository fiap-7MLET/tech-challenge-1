"""Rotas para estatísticas e insights sobre os livros (não implementadas)."""

from fastapi import APIRouter, Depends, status
from src.models.user import User
from src.services.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/overview", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def stats_overview(current_user: User = Depends(get_current_active_user)):
    """Estatísticas gerais da coleção (não implementado)."""
    return {"message": "Not implemented"}

@router.get("/categories", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def stats_categories(current_user: User = Depends(get_current_active_user)):
    """Estatísticas detalhadas por categoria (não implementado)."""
    return {"message": "Not implemented"}
