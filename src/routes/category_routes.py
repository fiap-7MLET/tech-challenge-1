"""Rotas para consulta de categorias de livros."""

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.extensions import get_db
from src.models.book import Book

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/")
def all_categories(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    """
    Lista todas as categorias de livros disponíveis com paginação.

    Args:
        request: Request object para construir URLs
        page: Número da página (padrão: 1)
        per_page: Quantidade de itens por página (padrão: 10)
        db: Sessão do banco de dados

    Returns:
        dict: Categorias paginadas com metadados de paginação
    """
    subquery = db.query(Book.category).distinct().order_by(Book.category)
    total = subquery.count()
    items = subquery.offset((page - 1) * per_page).limit(per_page).all()
    data = [{"name": category[0]} for category in items]
    total_pages = (total // per_page) + (1 if total % per_page else 0)

    base_url = str(request.url.remove_query_params(["page"]))
    next_url = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )
    prev_url = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None

    return {
        "data": data,
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": total_pages,
        "next": next_url,
        "previous": prev_url,
    }
