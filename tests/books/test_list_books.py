
def test_default_pagination_returns_five_books(client, seed_books):
    response = client.get("/api/v1/books/")
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert isinstance(data, list)
    assert len(data) == 5

def test_books_titles_are_correct(client, seed_books):
    response = client.get("/api/v1/books/")
    books = response.get_json()["data"]
    for i, book in enumerate(books, start=1):
        assert book["title"] == f"Book {i}"

def test_second_page_pagination(client, seed_books):
    response = client.get("/api/v1/books/?page=2")
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert len(data) >= 1
    assert data[0]["title"] == "Book 6"

def test_custom_per_page(client, seed_books):
    response = client.get("/api/v1/books/?per_page=2&page=2")
    data = response.get_json()["data"]
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == "Book 3"

def test_pagination(client, seed_books):
    response = client.get("/api/v1/books/?per_page=2&page=2")
    data = response.get_json()
    assert response.status_code == 200
    assert data["page"] == 2
    assert data["per_page"] == 2
    assert data["total"] == 6
    assert data["pages"] == 3
