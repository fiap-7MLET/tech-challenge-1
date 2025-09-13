
def test_default_pagination_returns_five_books(client, seed_books):
    response = client.get("/api/v1/categories/")
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert isinstance(data, list)
    assert len(data) == 3

def test_pagination(client, seed_books):
    response = client.get("/api/v1/categories/?per_page=2&page=1")
    data = response.get_json()
    assert response.status_code == 200
    assert data["page"] == 1
    assert data["per_page"] == 2
    assert data["total"] == 3
    assert data["pages"] == 2

def test_order(client, seed_books):
    response = client.get("/api/v1/categories/")
    data = response.get_json()
    assert response.status_code == 200
    data = response.get_json()["data"]
    print(data)
    assert data[0]["name"] == "Romance"
    assert data[1]["name"] == "Suspense"
    assert data[2]["name"] == "Terror"
