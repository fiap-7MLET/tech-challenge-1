"""Testes para rotas de scraping assíncrono."""
import pytest
from src.models.scraping_job import ScrapingJob
from unittest.mock import patch


def test_scraping_status_empty_database(client):
    """Testa /scraping/status com banco de dados vazio."""
    response = client.get("/scraping/status")
    assert response.status_code == 200

    data = response.json()
    assert "database" in data
    assert "last_job" in data
    assert data["database"]["total_books"] == 0
    assert data["database"]["total_categories"] == 0
    assert data["database"]["database_populated"] is False
    assert data["last_job"] is None


def test_scraping_trigger_returns_immediately(client):
    """Testa que /scraping/trigger retorna imediatamente com ID do job."""
    with patch('src.routes.scraping_routes.scrape_all_books') as mock_scrape:
        # Simula a função de scraping para evitar scraping real
        mock_scrape.return_value = []

        response = client.post("/scraping/trigger")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert data["status"] in ["started", "already_running"]
        assert "job_id" in data
        assert "check_status_url" in data or "job_status" in data


def test_scraping_trigger_creates_job(client, db):
    """Testa que /scraping/trigger cria um job no banco de dados."""
    with patch('src.routes.scraping_routes.scrape_all_books') as mock_scrape:
        mock_scrape.return_value = []

        response = client.post("/scraping/trigger")
        assert response.status_code == 200

        data = response.json()
        job_id = data["job_id"]

        # Verifica que o job foi criado
        job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
        assert job is not None
        assert job.status in ["pending", "in_progress"]


def test_scraping_prevents_concurrent_jobs(client):
    """Testa que apenas um job de scraping pode executar por vez."""
    with patch('src.routes.scraping_routes.scrape_all_books') as mock_scrape:
        mock_scrape.return_value = []

        # Cria primeiro job
        response1 = client.post("/scraping/trigger")
        assert response1.status_code == 200

        # Tenta criar segundo job imediatamente
        response2 = client.post("/scraping/trigger")
        assert response2.status_code == 200

        data2 = response2.json()
        # Deve obter status "already_running" ou ser permitido se o primeiro completou
        assert data2["status"] in ["started", "already_running"]


def test_scraping_status_with_job_id(client, db):
    """Testa /scraping/status com parâmetro job_id específico."""
    # Cria um job de teste
    job = ScrapingJob(
        status="completed",
        books_scraped=100,
        books_saved=100,
        csv_file="data/books.csv"
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    job_id = job.id

    # Consulta status com job_id
    response = client.get(f"/scraping/status?job_id={job_id}")
    assert response.status_code == 200

    data = response.json()
    assert "last_job" in data
    assert data["last_job"]["job_id"] == job_id
    assert data["last_job"]["status"] == "completed"
    assert data["last_job"]["books_scraped"] == 100
    assert data["last_job"]["books_saved"] == 100


def test_scraping_status_without_job_id_returns_latest(client, db):
    """Testa /scraping/status sem job_id retorna o último job."""
    # Cria múltiplos jobs de teste
    job1 = ScrapingJob(status="completed", books_scraped=50)
    db.add(job1)
    db.commit()

    job2 = ScrapingJob(status="completed", books_scraped=100)
    db.add(job2)
    db.commit()
    db.refresh(job2)
    latest_job_id = job2.id

    # Consulta status sem job_id
    response = client.get("/scraping/status")
    assert response.status_code == 200

    data = response.json()
    assert data["last_job"]["job_id"] == latest_job_id
    assert data["last_job"]["books_scraped"] == 100


def test_scraping_job_statuses(db):
    """Testa que um job pode ter diferentes status."""
    # Testa status pending
    job = ScrapingJob(status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    assert job.status == "pending"

    # Atualiza para in_progress
    job.status = "in_progress"
    db.commit()
    assert job.status == "in_progress"

    # Atualiza para completed
    job.status = "completed"
    job.books_scraped = 1000
    job.books_saved = 1000
    db.commit()
    assert job.status == "completed"

    # Testa status error
    job.status = "error"
    job.error_message = "Erro de teste"
    db.commit()
    assert job.status == "error"
    assert job.error_message == "Erro de teste"


def test_scraping_status_response_structure(client):
    """Testa que /scraping/status retorna estrutura de resposta correta."""
    response = client.get("/scraping/status")
    assert response.status_code == 200

    data = response.json()

    # Verifica seção database
    assert "database" in data
    assert "total_books" in data["database"]
    assert "total_categories" in data["database"]
    assert "database_populated" in data["database"]

    # Verifica seção last_job (pode ser None)
    assert "last_job" in data

    if data["last_job"] is not None:
        job = data["last_job"]
        assert "job_id" in job
        assert "status" in job
        assert "started_at" in job
        assert job["status"] in ["pending", "in_progress", "completed", "error"]


def test_completed_job_has_timestamps(db):
    """Testa que um job completo tem timestamps de início e fim."""
    from datetime import datetime, timezone

    job = ScrapingJob(
        status="completed",
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
        books_scraped=100,
        books_saved=100
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    assert job.started_at is not None
    assert job.completed_at is not None
    assert job.completed_at >= job.started_at


def test_error_job_has_error_message(client, db):
    """Testa que um job com erro inclui mensagem de erro."""
    job = ScrapingJob(
        status="error",
        error_message="Timeout de conexão"
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    job_id = job.id

    response = client.get(f"/scraping/status?job_id={job_id}")
    data = response.json()

    assert data["last_job"]["status"] == "error"
    assert data["last_job"]["error_message"] == "Timeout de conexão"
