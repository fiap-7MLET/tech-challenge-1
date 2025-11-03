"""Rotas para consulta e pesquisa de livros."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from src.api.schemas.book import BookSchema
from src.extensions import get_db
from src.models.book import Book

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=dict)
def all_books(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    """
    Lista todos os livros disponíveis no banco de dados com paginação.

    Args:
        request: Request object para construir URLs
        page: Número da página (padrão: 1)
        per_page: Quantidade de itens por página (padrão: 10)
        db: Sessão do banco de dados

    Returns:
        dict: Livros paginados com metadados de paginação
    """
    query = db.query(Book).order_by(Book.id)
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    total_pages = (total // per_page) + (1 if total % per_page else 0)

    base_url = str(request.url.remove_query_params(["page"]))
    next_url = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )
    prev_url = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None

    return {
        "data": [BookSchema.model_validate(book) for book in items],
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": total_pages,
        "next": next_url,
        "previous": prev_url,
    }


@router.get("/search", response_model=dict)
def search(
    request: Request,
    title: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    """
    Busca livros por título e/ou categoria com paginação.

    Args:
        request: Request object para construir URLs
        title: Título do livro para busca (opcional)
        category: Categoria do livro para busca (opcional)
        page: Número da página (padrão: 1)
        per_page: Quantidade de itens por página (padrão: 10)
        db: Sessão do banco de dados

    Returns:
        dict: Livros encontrados com metadados de paginação
    """
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(Book.category.ilike(f"%{category}%"))
    total = query.count()
    items = query.order_by(Book.id).offset((page - 1) * per_page).limit(per_page).all()
    total_pages = (total // per_page) + (1 if total % per_page else 0)

    base_url = str(request.url.remove_query_params(["page"]))
    next_url = f"{base_url}&page={page + 1}" if page < total_pages else None
    prev_url = f"{base_url}&page={page - 1}" if page > 1 else None

    return {
        "data": [BookSchema.model_validate(book) for book in items],
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": total_pages,
        "next": next_url,
        "previous": prev_url,
    }


@router.get("/top-rated", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def top_rated():
    """Lista os livros com melhor avaliação (não implementado)."""
    return {"message": "Not implemented"}


@router.get("/price-range", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def price_range(min: Optional[float] = Query(None), max: Optional[float] = Query(None)):
    """Filtra livros dentro de uma faixa de preço específica (não implementado)."""
    return {"message": "Not implemented"}


@router.get("/{book_id}", response_model=BookSchema)
def single_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes completos de um livro específico pelo ID.

    Args:
        book_id: ID do livro
        db: Sessão do banco de dados

    Returns:
        BookSchema: Detalhes do livro

    Raises:
        HTTPException: 404 se o livro não for encontrado
    """
    book = db.query(Book).filter_by(id=book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookSchema.model_validate(book)
