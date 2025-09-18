from fastapi import APIRouter
from pathlib import Path
from src.services.scraping.file_handler import update_books_data
from src.services.scraping.core import scrape_all_books

router = APIRouter()

@router.post("/trigger")
def trigger_scraping():
    """
    Dispara o processo de scraping dos livros sob demanda.
    """
    output_file = Path(__file__).parent.parent.parent.parent / "data" / "scraped_books.csv"
    sucesso = update_books_data(output_file, scraper_function=scrape_all_books)
    if sucesso:
        return {"mensagem": "Scraping realizado com sucesso."}
    return {"mensagem": "Falha ao realizar scraping."}
