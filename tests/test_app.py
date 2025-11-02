"""Testes de integração para os endpoints da aplicação."""


def test_health_route(client):
    response = client.get("/health/")
    assert response.status_code in [200, 500]
    assert "status" in response.json()
    assert "database" in response.json()


def test_books_route(client):
    response = client.get("/books/")
    assert response.status_code == 200
    assert "data" in response.json()
    assert "page" in response.json()
    assert "per_page" in response.json()
    assert "total" in response.json()
    assert "pages" in response.json()
    assert "next" in response.json()
    assert "previous" in response.json()


def test_categories_route(client):
    response = client.get("/categories/")
    assert response.status_code == 200
    assert "data" in response.json()
    assert "page" in response.json()
    assert "per_page" in response.json()
    assert "total" in response.json()
    assert "pages" in response.json()
    assert "next" in response.json()
    assert "previous" in response.json()


def test_auth_routes(client):
    for endpoint in ["/auth/register", "/auth/login", "/auth/logout", "/auth/refresh"]:
        response = client.post(endpoint)
        assert response.status_code == 501


def test_scraping_status_endpoint(client):
    response = client.get("/scraping/status")
    assert response.status_code == 200
    assert "database" in response.json()
    assert "last_job" in response.json()


def test_scraping_trigger_endpoint(client):
    response = client.post("/scraping/trigger")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "job_id" in response.json()
    # Status deve ser "started" ou "already_running"
    assert response.json()["status"] in ["started", "already_running"]
