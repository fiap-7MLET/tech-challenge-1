# tech-challenge-1
Projeto para o primeiro tech challenge da pós-tech da FIAP em Machine Learning

o projeto ainda não está fazendo nada, mas a estrutura de pastas no momento está desse jeito para mostrar onde deve ir o que, então deve seguir como o esqueleto da construção

poetry install

então:

poetry run python src/app.py

vai rodar a aplicação na porta 5000

então, ao rodar o curl

curl -w "%{http_code}\n" -X POST http://localhost:5000/api/v1/auth/register

vai retornar o 501, feito no routes/user_routes.py

para rodar os testes:

poetry run pytest