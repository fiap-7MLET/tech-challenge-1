# Tech Challenge 1 - API de Consulta de Livros

Projeto desenvolvido para o Tech Challenge da Fase 1 da Pós-Tech FIAP em Machine Learning Engineering.

## 📋 Sobre o Projeto

API REST pública desenvolvida com FastAPI para gerenciamento e consulta de catálogo de livros. O projeto inclui funcionalidade completa de web scraping para coleta automática de dados do site [books.toscrape.com](https://books.toscrape.com/), armazenamento em banco de dados SQLite e disponibilização via endpoints RESTful.

## 🎯 Objetivos do Projeto

- Desenvolver um pipeline completo de extração, transformação e disponibilização de dados
- Criar uma API pública escalável e reusável para futuros modelos de Machine Learning
- Implementar web scraping robusto com processamento assíncrono
- Fornecer endpoints RESTful bem documentados e testados

## 🚀 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido para construção de APIs
- **SQLAlchemy** - ORM para gerenciamento do banco de dados
- **httpx** - Cliente HTTP assíncrono para web scraping
- **BeautifulSoup4** - Parser HTML para extração de dados
- **Pydantic** - Validação de dados e serialização
- **Uvicorn** - Servidor ASGI de alta performance
- **Pytest** - Framework de testes
- **uv** - Gerenciador moderno de dependências e ambientes virtuais Python

## 📦 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- [uv](https://github.com/astral-sh/uv) instalado

### Passos de Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/fiap-7MLET/tech-challenge-1.git
cd tech-challenge-1

# 2. Instale as dependências usando uv
uv sync

# 3. (Opcional) Ative o ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

### Configuração de Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite:///db.sqlite3
DEBUG=False
```

## 🏃 Como Executar

### Iniciar o Servidor de Desenvolvimento

```bash
uv run uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

A aplicação estará disponível em:
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Popular o Banco de Dados

Antes de usar a API, popule o banco de dados com dados dos livros:

```bash
curl -X POST http://localhost:8000/scraping/trigger
```

Este comando irá:
1. Fazer scraping de aproximadamente 1000 livros do site books.toscrape.com
2. Salvar os dados no banco de dados SQLite
3. Gerar um arquivo CSV em `data/books.csv`
4. Retornar estatísticas da operação

## 🔧 Endpoints da API

### Endpoints Principais (Obrigatórios)

#### Health Check
- **GET** `/health/` - Verifica o status da API e conectividade com o banco de dados

#### Livros
- **GET** `/books/` - Lista todos os livros com paginação
  - Query params: `page` (default: 1), `per_page` (default: 5)
- **GET** `/books/{id}` - Retorna detalhes de um livro específico
- **GET** `/books/search` - Busca livros por título e/ou categoria
  - Query params: `title`, `category`, `page`, `per_page`

#### Categorias
- **GET** `/categories/` - Lista todas as categorias disponíveis com paginação
  - Query params: `page` (default: 1), `per_page` (default: 5)

#### Scraping
- **POST** `/scraping/trigger` - Dispara o processo de scraping e popula o banco de dados
- **GET** `/scraping/status` - Retorna estatísticas do banco de dados (total de livros, categorias, etc.)

### Endpoints Opcionais (Bônus)

#### Estatísticas (Não Implementados)
- **GET** `/stats/overview` - Estatísticas gerais da coleção
- **GET** `/stats/categories` - Estatísticas detalhadas por categoria

#### Livros Extras (Não Implementados)
- **GET** `/books/top-rated` - Livros com melhor avaliação
- **GET** `/books/price-range` - Filtra livros por faixa de preço

#### Machine Learning (Não Implementados)
- **GET** `/ml/features` - Dados formatados para features de ML
- **GET** `/ml/training-data` - Dataset para treinamento
- **POST** `/ml/predictions` - Endpoint para receber predições

#### Autenticação (Não Implementado)
- **POST** `/auth/register` - Registro de usuário
- **POST** `/auth/login` - Login de usuário
- **POST** `/auth/logout` - Logout de usuário
- **POST** `/auth/refresh` - Renovação de token

## 🌐 Exemplos de Uso

### Verificar Status da API

```bash
curl http://localhost:8000/health/
```

### Listar Livros (com paginação)

```bash
curl "http://localhost:8000/books/?page=1&per_page=10"
```

### Buscar Livro por ID

```bash
curl "http://localhost:8000/books/1"
```

### Buscar Livros por Título

```bash
curl "http://localhost:8000/books/search?title=python&page=1&per_page=5"
```

### Buscar Livros por Categoria

```bash
curl "http://localhost:8000/books/search?category=Fiction&page=1&per_page=5"
```

### Listar Todas as Categorias

```bash
curl "http://localhost:8000/categories/?page=1&per_page=20"
```

### Verificar Status do Scraping

```bash
curl "http://localhost:8000/scraping/status"
```

## 📁 Estrutura do Projeto

```
tech-challenge-1/
├── src/
│   ├── api/
│   │   └── schemas/          # Schemas Pydantic para validação
│   │       └── book.py
│   ├── models/                # Modelos SQLAlchemy
│   │   ├── book.py
│   │   └── user.py
│   ├── routes/                # Rotas da API (endpoints)
│   │   ├── book_routes.py
│   │   ├── category_routes.py
│   │   ├── health_routes.py
│   │   ├── scraping_routes.py
│   │   ├── stats_routes.py
│   │   ├── ml_routes.py
│   │   └── user_routes.py
│   ├── services/
│   │   └── scraping/         # Lógica de web scraping
│   │       ├── core.py       # Scraper assíncrono principal
│   │       └── file_handler.py  # Manipulação de arquivos CSV
│   ├── extensions.py          # Configuração do banco de dados
│   ├── conf.py                # Configurações gerais
│   └── app.py                 # Aplicação principal FastAPI
├── data/                      # Dados gerados (CSV)
├── migrations/                # Migrations do banco de dados
├── tests/                     # Testes automatizados
├── pyproject.toml            # Configuração de dependências (uv/pip)
├── uv.lock                   # Lock file do uv
├── Tech_Challenge_API.postman_collection.json  # Coleção Postman
└── README.md                 # Este arquivo
```

## 🗄️ Banco de Dados

### Modelo de Dados

O projeto utiliza SQLite como banco de dados com a seguinte estrutura:

**Tabela: books**
- `id` (Integer, PK) - Identificador único
- `title` (String) - Título do livro (único)
- `price` (Numeric) - Preço do livro
- `rating` (Integer) - Avaliação de 1 a 5
- `availability` (Boolean) - Disponibilidade em estoque
- `category` (String) - Categoria do livro
- `image` (String) - URL da imagem

### Gerenciamento do Banco

O banco de dados é criado automaticamente na primeira execução em `db.sqlite3`.

## 🕷️ Web Scraping

### Características do Scraper

- **Assíncrono**: Utiliza `httpx` e `asyncio` para máxima performance
- **Robusto**: Tratamento de erros e retry automático
- **Completo**: Extrai todos os campos necessários (título, preço, rating, categoria, imagem)
- **Escalável**: Processa múltiplas páginas em paralelo
- **Logging**: Registra progresso e erros durante a execução

### Fonte de Dados

- **URL**: https://books.toscrape.com/
- **Campos Extraídos**:
  - Título do livro
  - Preço (em libras)
  - Rating (1-5 estrelas)
  - Disponibilidade em estoque
  - Categoria
  - URL da imagem

## 🧪 Testes

### Executar Testes

```bash
# Executar todos os testes
uv run pytest

# Executar com output detalhado
uv run pytest -v

# Executar com cobertura de código
uv run pytest --cov=src --cov-report=html
```

### Cobertura de Testes

O projeto inclui testes para:
- ✅ Rotas da API
- ✅ Modelos de dados
- ✅ Schemas Pydantic
- ✅ Funções de scraping
- ✅ Manipulação de arquivos CSV

## 📊 Coleção Postman

Uma coleção Postman completa está disponível em `Tech_Challenge_API.postman_collection.json` com todos os endpoints configurados e exemplos de requisições.

### Importar no Postman

1. Abra o Postman
2. Clique em "Import"
3. Selecione o arquivo `Tech_Challenge_API.postman_collection.json`
4. A coleção estará disponível com todos os endpoints pré-configurados

## 🏗️ Arquitetura e Pipeline de Dados

### Fluxo de Dados

```
[books.toscrape.com]
    ↓ (Web Scraping - httpx + BeautifulSoup)
[Dados Brutos]
    ↓ (Transformação e Limpeza)
[Dados Estruturados]
    ↓ (Armazenamento Dual)
    ├→ [SQLite Database] → [FastAPI] → [Endpoints REST] → [Consumidores]
    └→ [CSV File] → [Análise/ML]
```

### Escalabilidade Futura

A arquitetura foi desenhada pensando em:
- **Modularidade**: Componentes independentes e reutilizáveis
- **Extensibilidade**: Fácil adição de novos endpoints e funcionalidades
- **ML-Ready**: Estrutura preparada para integração com modelos de ML
- **Cache**: Possibilidade de adicionar camada de cache (Redis)
- **Queue**: Preparado para adicionar filas de processamento (Celery)

## 🎓 Cenário de Uso para ML

Esta API foi desenvolvida pensando em servir como base para:
1. **Sistemas de Recomendação**: Dados estruturados de livros, categorias e ratings
2. **Análise de Preços**: Histórico e comparação de preços
3. **Classificação de Texto**: Categorização automática baseada em títulos
4. **Feature Engineering**: Endpoints preparados para exportar features

## 👥 Equipe

Desenvolvido como parte do Tech Challenge - Fase 1
Pós-Tech FIAP - Machine Learning Engineering

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Observação**: Este projeto foi desenvolvido para fins educacionais como parte do Tech Challenge da FIAP.
