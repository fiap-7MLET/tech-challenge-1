"""Rotas para integração com Machine Learning (não implementadas)."""

from fastapi import APIRouter, status

router = APIRouter(prefix="/ml", tags=["ml"])


@router.get("/features", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def ml_features():
    """Dados formatados para features de modelos de ML (não implementado)."""
    return {"message": "Not implemented"}


@router.get("/training-data", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def ml_training_data():
    """Dataset para treinamento de modelos de ML (não implementado)."""
    return {"message": "Not implemented"}


@router.post("/predictions", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def ml_predictions():
    """Endpoint para receber predições de modelos de ML (não implementado)."""
    return {"message": "Not implemented"}
