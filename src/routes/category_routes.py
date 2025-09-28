
# Migração para FastAPI
from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from fastapi import Depends

from models.book import Book
from src.extensions import get_db

router = APIRouter(prefix="/categories", tags=["categories"])



@router.get("/")
def all_categories(
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1),
    db: Session = Depends(get_db)
):
    subquery = db.query(Book.category).distinct().order_by(Book.category)
    total = subquery.count()
    items = subquery.offset((page - 1) * per_page).limit(per_page).all()
    data = [{"name": category[0]} for category in items]
    return {
        "data": data,
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total // per_page) + (1 if total % per_page else 0)
    }