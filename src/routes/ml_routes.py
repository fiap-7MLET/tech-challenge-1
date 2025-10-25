"""Rotas para integração com Machine Learning (não implementadas)."""

from fastapi import APIRouter, Depends, status
from src.models.user import User
from src.services.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/ml", tags=["ml"])

@router.get("/features", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def ml_features(current_user: User = Depends(get_current_active_user)):
    """Dados formatados para features de modelos de ML (não implementado)."""
    return {"message": "Not implemented"}

@router.get("/training-data", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def ml_training_data(current_user: User = Depends(get_current_active_user)):
    """Dataset para treinamento de modelos de ML (não implementado)."""
    return {"message": "Not implemented"}

@router.post("/predictions", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def ml_predictions(current_user: User = Depends(get_current_active_user)):
    """Endpoint para receber predições de modelos de ML (não implementado)."""
    return {"message": "Not implemented"}
