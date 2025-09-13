
def test_get_existing_book(client, seed_books):
    book = seed_books[0]
    response = client.get(f"/api/v1/books/{book.id}")
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["id"] == book.id
    assert data["title"] == book.title
    assert data["price"] == float(book.price)
    assert data["rating"] == book.rating
    assert data["availability"] == book.availability
    assert data["category"] == book.category

def test_get_non_existing_book(client):
    response = client.get("/api/v1/books/9999") 
    assert response.status_code == 404
    assert response.get_json()["error"] == "Book not found"