from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from src.extensions import get_db
from src.models.book import Book
from src.services.scraping import scrape_all_books
from src.services.scraping.file_handler import save_books_to_csv
from typing import Dict, Any
import logging
import pathlib

router = APIRouter(prefix="/scraping", tags=["scraping"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_books_to_db(db: Session, books_data: list[Dict[str, Any]]) -> int:
    """
    Salva os dados dos livros coletados no banco de dados.

    Args:
        db: Sessão do banco de dados
        books_data: Lista de dicionários com os dados dos livros

    Returns:
        Número de livros salvos
    """
    saved_count = 0

    for book_data in books_data:
        try:
            # Verifica se o livro já existe
            existing_book = db.query(Book).filter(
                Book.title == book_data["title"]
            ).first()

            if existing_book:
                # Atualiza o livro existente
                existing_book.price = book_data["price"]
                existing_book.rating = book_data["rating"]
                existing_book.availability = "In stock" in book_data.get("availability", "")
                existing_book.category = book_data["category"]
                existing_book.image = book_data.get("image_url")
                db.commit()
            else:
                # Cria um novo livro
                new_book = Book(
                    title=book_data["title"],
                    price=book_data["price"],
                    rating=book_data["rating"],
                    availability="In stock" in book_data.get("availability", ""),
                    category=book_data["category"],
                    image=book_data.get("image_url")
                )
                db.add(new_book)
                db.commit()

            saved_count += 1

        except Exception as e:
            logger.error(f"Erro ao salvar livro '{book_data.get('title', 'unknown')}': {e}")
            db.rollback()
            continue

    return saved_count


@router.post("/trigger")
def trigger_scraping(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Endpoint para disparar o scraping de livros e popular o banco de dados e CSV.

    O scraping é executado de forma síncrona e os dados são salvos no banco e em arquivo CSV.

    Returns:
        Dicionário com o status da operação e quantidade de livros processados
    """
    try:
        logger.info("Iniciando scraping de livros...")

        # Executa o scraping
        books_data = scrape_all_books()

        if not books_data:
            raise HTTPException(
                status_code=500,
                detail="Nenhum dado foi coletado durante o scraping"
            )

        logger.info(f"Scraping concluído. {len(books_data)} livros coletados.")

        # Salva no banco de dados
        saved_count = save_books_to_db(db, books_data)

        # Salva em arquivo CSV
        csv_file = pathlib.Path("data/books.csv")
        csv_saved = save_books_to_csv(csv_file, books_data)

        return {
            "status": "success",
            "message": f"Scraping concluído com sucesso",
            "books_scraped": len(books_data),
            "books_saved_db": saved_count,
            "csv_saved": csv_saved,
            "csv_file": str(csv_file) if csv_saved else None
        }

    except Exception as e:
        logger.error(f"Erro durante o scraping: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro durante o scraping: {str(e)}"
        )


@router.get("/status")
def scraping_status(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Retorna o status atual do banco de dados de livros.

    Returns:
        Dicionário com estatísticas do banco de dados
    """
    total_books = db.query(Book).count()
    categories = db.query(Book.category).distinct().count()

    return {
        "total_books": total_books,
        "total_categories": categories,
        "database_populated": total_books > 0
    }
