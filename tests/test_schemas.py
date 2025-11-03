from src.api.schemas.book import BookSchema, UserSchema


def test_book_schema_fields():
    data = {
        "id": 1,
        "title": "Livro Teste",
        "price": 10.0,
        "rating": 5,
        "availability": True,
        "category": "Ficção",
        "image": "img.png",
    }
    schema = BookSchema(**data)
    for key in data:
        assert getattr(schema, key) == data[key]


def test_user_schema_fields():
    data = {"id": 1, "email": "teste@teste.com", "password": "123456"}
    schema = UserSchema(**data)
    for key in data:
        assert getattr(schema, key) == data[key]
