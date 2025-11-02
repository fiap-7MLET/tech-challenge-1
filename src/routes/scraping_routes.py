from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from src.extensions import get_db
from src.models.book import Book
from src.models.scraping_job import ScrapingJob
from src.services.scraping import scrape_all_books
from src.services.scraping.file_handler import save_books_to_csv
from typing import Dict, Any
from datetime import datetime, timezone
import logging
import pathlib

router = APIRouter(prefix="/scraping", tags=["scraping"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_scraping_job(job_id: int):
    """
    Executa o job de scraping em background.

    Args:
        job_id: ID do job de scraping
    """
    from src.extensions import SessionLocal
    db = SessionLocal()

    try:
        # Busca o job
        job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
        if not job:
            logger.error(f"Job {job_id} não encontrado")
            return

        # Atualiza status para in_progress
        job.status = "in_progress"
        db.commit()

        logger.info(f"Iniciando scraping job {job_id}...")

        # Executa o scraping
        books_data = scrape_all_books()

        if not books_data:
            job.status = "error"
            job.error_message = "Nenhum dado foi coletado durante o scraping"
            job.completed_at = datetime.now(timezone.utc)
            db.commit()
            logger.error(f"Job {job_id} falhou: nenhum dado coletado")
            return

        logger.info(f"Job {job_id}: {len(books_data)} livros coletados")

        # Salva no banco de dados
        saved_count = save_books_to_db(db, books_data)

        # Salva em arquivo CSV
        csv_file = pathlib.Path("data/books.csv")
        csv_saved = save_books_to_csv(csv_file, books_data)

        # Atualiza job como completo
        job.status = "completed"
        job.completed_at = datetime.now(timezone.utc)
        job.books_scraped = len(books_data)
        job.books_saved = saved_count
        job.csv_file = str(csv_file) if csv_saved else None
        db.commit()

        logger.info(f"Job {job_id} concluído com sucesso")

    except Exception as e:
        logger.error(f"Erro durante scraping job {job_id}: {e}")
        try:
            job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
            if job:
                job.status = "error"
                job.error_message = str(e)
                job.completed_at = datetime.now(timezone.utc)
                db.commit()
        except Exception as update_error:
            logger.error(f"Erro ao atualizar status do job {job_id}: {update_error}")
    finally:
        db.close()


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
    Endpoint para disparar o scraping de livros de forma assíncrona.

    O scraping é executado em background e o status pode ser consultado
    via endpoint /scraping/status.

    Returns:
        Dicionário com o ID do job criado e informações para acompanhamento
    """
    try:
        # Verifica se já existe um job em andamento
        active_job = db.query(ScrapingJob).filter(
            ScrapingJob.status.in_(["pending", "in_progress"])
        ).first()

        if active_job:
            return {
                "status": "already_running",
                "message": "Já existe um job de scraping em andamento",
                "job_id": active_job.id,
                "job_status": active_job.status
            }

        # Cria um novo job
        new_job = ScrapingJob(
            status="pending",
            started_at=datetime.now(timezone.utc)
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)

        # Adiciona o job à fila de background tasks
        background_tasks.add_task(run_scraping_job, new_job.id)

        logger.info(f"Job de scraping {new_job.id} criado e adicionado à fila")

        return {
            "status": "started",
            "message": "Scraping iniciado em background",
            "job_id": new_job.id,
            "check_status_url": f"/scraping/status?job_id={new_job.id}"
        }

    except Exception as e:
        logger.error(f"Erro ao criar job de scraping: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar job de scraping: {str(e)}"
        )


@router.get("/status")
def scraping_status(
    job_id: int = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Retorna o status do scraping.

    Args:
        job_id: ID do job específico (opcional). Se não fornecido, retorna o último job.

    Returns:
        Dicionário com o status do job e estatísticas do banco de dados
    """
    # Estatísticas do banco de dados
    total_books = db.query(Book).count()
    total_categories = db.query(Book.category).distinct().count()

    # Busca informações do job
    if job_id:
        job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
    else:
        # Pega o job mais recente
        job = db.query(ScrapingJob).order_by(ScrapingJob.started_at.desc()).first()

    response = {
        "database": {
            "total_books": total_books,
            "total_categories": total_categories,
            "database_populated": total_books > 0
        }
    }

    if job:
        job_info = {
            "job_id": job.id,
            "status": job.status,
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "books_scraped": job.books_scraped,
            "books_saved": job.books_saved,
            "csv_file": job.csv_file,
            "error_message": job.error_message
        }
        response["last_job"] = job_info
    else:
        response["last_job"] = None

    return response
