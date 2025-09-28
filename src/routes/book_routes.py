from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from models.book import Book
from sqlalchemy.orm import Session
from src.extensions import get_db
from src.api.schemas.book import BookSchema

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=dict)
def all_books(page: int = Query(1, ge=1), per_page: int = Query(5, ge=1), db: Session = Depends(get_db)):
    query = db.query(Book).order_by(Book.id)
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return {
    "data": [BookSchema.model_validate(book) for book in items],
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total // per_page) + (1 if total % per_page else 0)
    }

@router.get("/{book_id}", response_model=BookSchema)
def single_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter_by(id=book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookSchema.model_validate(book)

@router.get("/search", response_model=dict)
def search(
    title: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1),
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(Book.category.ilike(f"%{category}%"))
    total = query.count()
    items = query.order_by(Book.id).offset((page - 1) * per_page).limit(per_page).all()
    return {
    "data": [BookSchema.model_validate(book) for book in items],
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total // per_page) + (1 if total % per_page else 0)
    }