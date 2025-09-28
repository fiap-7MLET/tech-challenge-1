
# Migração para FastAPI
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.extensions import SessionLocal
from sqlalchemy import select, literal_column

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health():
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
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR if error else status.HTTP_200_OK,
        content={
            "status": status_,
            "database": db_status
        }
    )