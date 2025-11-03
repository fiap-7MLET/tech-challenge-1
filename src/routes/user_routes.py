"""Rotas de autenticação de usuários (não implementadas)."""

from fastapi import APIRouter, status

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def register():
    """Endpoint de registro de usuário (não implementado)."""
    return ""


@router.post("/login", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def login():
    """Endpoint de login de usuário (não implementado)."""
    return ""


@router.post("/logout", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def logout():
    """Endpoint de logout de usuário (não implementado)."""
    return ""


@router.post("/refresh", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def refresh():
    """Endpoint de renovação de token (não implementado)."""
    return ""
