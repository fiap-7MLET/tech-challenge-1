import csv
import logging
import pathlib
from typing import Any, Callable, Dict, List

from .core import scrape_all_books

# Configuração do logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def save_books_to_csv(
    output_file: pathlib.Path, books_data: List[Dict[str, Any]]
) -> bool:
    """Salva os dados dos livros em um arquivo CSV.

    Args:
        output_file: Caminho do arquivo CSV onde os dados serão salvos
        books_data: Lista de dicionários contendo os dados dos livros

    Returns:
        bool: True se os dados foram salvos com sucesso, False caso contrário
    """
    # Garante que o diretório de saída existe
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if not books_data:
        logging.warning("Nenhum dado disponível para salvar.")
        return False

    # Define os cabeçalhos para garantir a ordem consistente das colunas
    headers = [
        "title",
        "price",
        "rating",
        "availability",
        "category",
        "image_url",
    ]

    try:
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(books_data)
        logging.info(f"Dados salvos com sucesso no arquivo {output_file}")
        return True
    except IOError as e:
        logging.error(f"Erro ao salvar o arquivo: {e}")
        return False


def update_books_data(
    output_file: pathlib.Path,
    scraper_function: Callable[[], List[Dict[str, Any]]] = scrape_all_books,
) -> bool:
    """Atualiza o arquivo CSV com os dados mais recentes dos livros.

    Args:
        output_file: Caminho do arquivo CSV onde os dados serão salvos
        scraper_function: Função a ser usada para coletar os dados dos livros
            (padrão: scrape_all_books)

    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário
    """
    logging.info("Iniciando o processo de coleta de dados dos livros...")
    books_data = scraper_function()

    if not books_data:
        logging.warning("Nenhum dado foi coletado.")
        return False

    logging.info(f"Coleta concluída. Foram encontrados {len(books_data)} livros.")
    return save_books_to_csv(output_file, books_data)
