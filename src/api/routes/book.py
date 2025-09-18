from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.api.schemas.book import BookCreate, BookRead
from src.extensions import get_db
from src.models.book import Book

router = APIRouter()

@router.post("/", response_model=BookRead)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Cria um novo livro.
    """
    db_book = db.query(Book).filter(Book.title == book.title).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Livro já cadastrado.")
    novo_livro = Book(**book.dict())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro

@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retorna os dados de um livro pelo ID.
    """
    livro = db.query(Book).filter(Book.id == book_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return livro
