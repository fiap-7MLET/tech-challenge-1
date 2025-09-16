import httpx
import asyncio
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Optional, Dict, Any, List


def clean_title(title: str) -> str:
    """Limpa o título do livro removendo caracteres problemáticos para CSV."""
    return title.replace(",", "").strip()


# Configuração do logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


async def fetch_page(client: httpx.AsyncClient, url: str) -> Optional[str]:
    """Busca o conteúdo de uma única página de forma assíncrona.
    
    Args:
        client: Cliente HTTP assíncrono
        url: URL da página a ser buscada
        
    Returns:
        O conteúdo HTML da página ou None em caso de erro
    """
    try:
        response = await client.get(url, headers=HEADERS, follow_redirects=True)
        response.raise_for_status()
        return response.text
    except httpx.RequestError as e:
        logging.error(f"Falha ao buscar a URL {url}: {e}")
        return None


def parse_book_details(
    html_content: str, book_url: str
) -> Optional[Dict[str, Any]]:
    """Analisa os detalhes de um livro a partir do conteúdo HTML de sua página.
    
    Args:
        html_content: Conteúdo HTML da página do livro
        book_url: URL da página do livro (usado para logging em caso de erro)
        
    Returns:
        Dicionário com os detalhes do livro ou None em caso de erro
    """
    soup = BeautifulSoup(html_content, "html.parser")
    try:
        title = clean_title(soup.find("h1").text)
        price_str = soup.find("p", class_="price_color").text
        price = float(price_str.replace("£", "").replace("Â", ""))

        rating_tag = soup.find("p", class_="star-rating")
        rating_class = rating_tag["class"][-1] if rating_tag else "Zero"
        rating = RATING_MAP.get(rating_class, 0)

        availability_tag = soup.find("p", class_="instock availability")
        availability = (
            availability_tag.text.strip() if availability_tag else "N/A"
        )

        category_tag = soup.select_one("ul.breadcrumb li:nth-of-type(3) a")
        category = category_tag.text.strip() if category_tag else "N/A"

        image_tag = soup.select_one("#product_gallery .item img")
        relative_img_url = image_tag["src"]
        image_url = urljoin(BASE_URL, relative_img_url)

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "category": category,
            "image_url": image_url,
        }
    except (AttributeError, IndexError, ValueError) as e:
        logging.error(f"Erro ao analisar detalhes do livro em {book_url}: {e}")
        return None


async def scrape_book_task(
    client: httpx.AsyncClient, book_url: str
) -> Optional[Dict[str, Any]]:
    """Tarefa assíncrona para buscar e analisar os detalhes de um único livro.
    
    Args:
        client: Cliente HTTP assíncrono
        book_url: URL da página do livro
        
    Returns:
        Dicionário com os detalhes do livro ou None em caso de erro
    """
    html_content = await fetch_page(client, book_url)
    if html_content:
        return parse_book_details(html_content, book_url)
    return None


async def scrape_all_books_async() -> List[Dict[str, Any]]:
    """Lógica principal de scraping assíncrono para todos os livros.
    
    Busca todas as páginas do catálogo de forma assíncrona e coleta os detalhes
    de cada livro encontrado.
    
    Returns:
        Lista de dicionários, onde cada dicionário contém os detalhes de um livro
    """
    all_books_data = []
    current_url = urljoin(BASE_URL, "catalogue/page-1.html")

    async with httpx.AsyncClient() as client:
        while current_url:
            logging.info(f"Coletando dados da página: {current_url}")
            main_page_content = await fetch_page(client, current_url)

            if not main_page_content:
                break

            soup = BeautifulSoup(main_page_content, "html.parser")
            book_links = [
                urljoin(current_url, a["href"]) for a in soup.select("h3 a")
            ]

            tasks = [scrape_book_task(client, link) for link in book_links]
            results = await asyncio.gather(*tasks)

            page_books_data = [book for book in results if book]
            all_books_data.extend(page_books_data)

            next_page_tag = soup.select_one("li.next a")
            if next_page_tag and next_page_tag.has_attr("href"):
                current_url = urljoin(current_url, next_page_tag["href"])
            else:
                logging.info("Coleta de dados concluída. Todas as páginas foram processadas.")
                current_url = None

    return all_books_data


def scrape_all_books() -> List[Dict[str, Any]]:
    """Wrapper síncrono para o scraper assíncrono.
    
    Esta função é o ponto de entrada principal para o scraping,
    encapsulando toda a lógica assíncrona em uma interface síncrona.
    
    Returns:
        Lista de dicionários, onde cada dicionário contém os detalhes de um livro
    """
    return asyncio.run(scrape_all_books_async())
