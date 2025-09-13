
def test_search_by_title(client, seed_books):
    response = client.get("/api/v1/books/search?title=Book 1")
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Book 1"
    
def test_search_by_category(client, seed_books):
    response = client.get("/api/v1/books/search?category=Suspense")
    data = response.get_json()["data"]
    assert response.status_code == 200
    assert len(data) == 2
    for book in data:
        assert "Suspense" == book["category"]

def test_search_by_title_and_category(client, seed_books):
    response = client.get("/api/v1/books/search?title=Book 1&category=Suspense")
    data = response.get_json()["data"]

    assert response.status_code == 200
    for book in data:
        assert "Book 1" in book["title"]
        assert "Suspense" in book["category"]

def test_pagination_default(client, seed_books):
    response = client.get("/api/v1/books/search")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["page"] == 1
    assert json_data["per_page"] == 5
    assert len(json_data["data"]) == 5