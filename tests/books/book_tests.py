
def test_list_books(client, seed_books):
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    assert len(response.json) >= 5
