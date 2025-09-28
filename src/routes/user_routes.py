
# Migração para FastAPI
from fastapi import APIRouter, status

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def register():
    return ""

@router.post("/login", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def login():
    return ""

@router.post("/logout", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def logout():
    return ""

@router.post("/refresh", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def refresh():
    return ""
