# Tech Challenge 1 - API de Consulta de Livros

Projeto desenvolvido para o Tech Challenge da Fase 1 da Pós-Tech FIAP em Machine Learning Engineering.

## 📋 Sobre o Projeto

API REST pública desenvolvida com FastAPI para gerenciamento e consulta de catálogo de livros. O projeto inclui funcionalidade completa de web scraping para coleta automática de dados do site [books.toscrape.com](https://books.toscrape.com/), armazenamento em banco de dados SQLite e disponibilização via endpoints RESTful.

## 🎯 Objetivos do Projeto

- Desenvolver um pipeline completo de extração, transformação e disponibilização de dados
- Criar uma API escalável e reusável para futuros modelos de Machine Learning
- Implementar web scraping robusto com processamento assíncrono
- Fornecer endpoints RESTful bem documentados e testados
- **[BONUS]** Implementar sistema de autenticação JWT completo com controle de acesso

## 🚀 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido para construção de APIs
- **SQLAlchemy** - ORM para gerenciamento do banco de dados
- **httpx** - Cliente HTTP assíncrono para web scraping
- **BeautifulSoup4** - Parser HTML para extração de dados
- **Pydantic** - Validação de dados e serialização
- **Uvicorn** - Servidor ASGI de alta performance
- **Pytest** - Framework de testes
- **uv** - Gerenciador moderno de dependências e ambientes virtuais Python
- **JWT (JSON Web Tokens)** - Autenticação e autorização segura
- **Bcrypt** - Hash de senhas com segurança

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
SECRET_KEY=your-secret-key-change-in-production
DEBUG=False
```

**IMPORTANTE**: Gere uma chave secreta segura para produção:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
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

### Executar Migrações do Banco de Dados

Antes de usar a API, execute as migrações para criar as tabelas:

```bash
uv run alembic upgrade head
```

### Popular o Banco de Dados

Para popular o banco de dados, você precisa primeiro se registrar como usuário admin e depois disparar o scraping:

```bash
# 1. Registrar primeiro usuário (automaticamente se torna admin)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "AdminPass123"}'

# 2. Salvar o token retornado e usar para disparar scraping
curl -X POST http://localhost:8000/scraping/trigger \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

Este comando irá:
1. Fazer scraping de aproximadamente 1000 livros do site books.toscrape.com
2. Salvar os dados no banco de dados SQLite
3. Gerar um arquivo CSV em `data/books.csv`
4. Retornar estatísticas da operação

**Nota**: O endpoint `/scraping/trigger` requer privilégios de administrador.

## 🔧 Endpoints da API

### 🔓 Endpoints Públicos (Sem Autenticação)

#### Health Check
- **GET** `/health/` - Verifica o status da API e conectividade com o banco de dados

### 🔐 Endpoints de Autenticação

#### Registro e Login
- **POST** `/api/v1/auth/register` - Registro de novo usuário
  - Primeiro usuário registrado automaticamente se torna admin
  - Requisitos de senha: mínimo 8 caracteres, 1 maiúscula, 1 minúscula, 1 dígito
  - Retorna: `access_token`, `refresh_token`, `token_type`
- **POST** `/api/v1/auth/login` - Login de usuário existente (OAuth2 password flow)
  - Retorna: `access_token`, `refresh_token`, `token_type`
- **POST** `/api/v1/auth/refresh` - Renovação de tokens usando refresh token
  - Retorna: novos `access_token` e `refresh_token`
- **GET** `/api/v1/auth/me` - Informações do usuário atual (requer autenticação)

#### Gerenciamento de Usuários (Admin)
- **GET** `/api/v1/auth/users` - **[ADMIN ONLY]** Lista todos os usuários registrados
  - Retorna: array com id, email, is_active, is_admin, created_at
- **POST** `/api/v1/auth/users/{user_id}/promote` - **[ADMIN ONLY]** Promove usuário a admin
  - Retorna: informações do usuário atualizado
  - Validações: usuário existe, não é admin ainda
- **POST** `/api/v1/auth/users/{user_id}/demote` - **[ADMIN ONLY]** Remove privilégios de admin
  - Retorna: informações do usuário atualizado
  - Validações: usuário existe, é admin, não pode se rebaixar (proteção contra lockout)

### 🔒 Endpoints Protegidos (Requerem Autenticação)

**Todos os endpoints abaixo requerem header de autenticação:**
```
Authorization: Bearer SEU_ACCESS_TOKEN
```

#### Livros
- **GET** `/books/` - Lista todos os livros com paginação
  - Query params: `page` (default: 1), `per_page` (default: 10)
  - Resposta inclui URLs de navegação: `next`, `previous`
- **GET** `/books/{id}` - Retorna detalhes de um livro específico
- **GET** `/books/search` - Busca livros por título e/ou categoria
  - Query params: `title`, `category`, `page`, `per_page`
  - Resposta inclui URLs de navegação: `next`, `previous`

#### Categorias
- **GET** `/categories/` - Lista todas as categorias disponíveis com paginação
  - Query params: `page` (default: 1), `per_page` (default: 10)
  - Resposta inclui URLs de navegação: `next`, `previous`

#### Scraping
- **GET** `/scraping/status` - Retorna estatísticas do banco de dados (total de livros, categorias, etc.)
- **POST** `/scraping/trigger` - **[ADMIN ONLY]** Dispara o processo de scraping e popula o banco de dados

#### Estatísticas (Endpoints Preparados)
- **GET** `/stats/overview` - Estatísticas gerais da coleção
- **GET** `/stats/categories` - Estatísticas detalhadas por categoria

#### Machine Learning (Endpoints Preparados)
- **GET** `/ml/features` - Dados formatados para features de ML
- **GET** `/ml/training-data` - Dataset para treinamento
- **POST** `/ml/predictions` - Endpoint para receber predições

### 🔑 Sistema de Autenticação

A API implementa autenticação JWT (JSON Web Tokens) completa com:

- **Access Tokens**: Válidos por 10 minutos
- **Refresh Tokens**: Válidos por 5 minutos (podem ser usados para obter novos tokens)
- **Roles**: Admin e Regular User
- **Segurança**: Senhas hasheadas com Bcrypt
- **OAuth2 Compliance**: Segue padrão OAuth2 Password Flow

#### Como Usar Autenticação

1. **Registrar um usuário:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "SecurePass123"}'
```

2. **Fazer login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=SecurePass123"
```

3. **Usar o token em requisições:**
```bash
curl http://localhost:8000/books/ \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

4. **Renovar token expirado:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "SEU_REFRESH_TOKEN"}'
```

#### Gerenciamento de Admin

Admins podem gerenciar outros usuários:

1. **Listar todos os usuários:**
```bash
curl http://localhost:8000/api/v1/auth/users \
  -H "Authorization: Bearer TOKEN_DO_ADMIN"
```

2. **Promover usuário a admin:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/users/2/promote \
  -H "Authorization: Bearer TOKEN_DO_ADMIN"
```

3. **Remover privilégios de admin:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/users/2/demote \
  -H "Authorization: Bearer TOKEN_DO_ADMIN"
```

**Nota de Segurança**: Admins não podem se rebaixar para prevenir lockout do sistema.

## 🌐 Exemplos de Uso

A API pode ser testada de duas formas: via **linha de comando (curl)** ou via **Swagger UI (interface gráfica)**. Recomendamos usar o Swagger UI para exploração inicial, pois oferece documentação interativa e validação automática.

### 📖 Acessando a Documentação Interativa

**Swagger UI**: http://localhost:8000/docs
**ReDoc**: http://localhost:8000/redoc

### 🔐 Autenticando no Swagger UI

Para testar endpoints protegidos no Swagger UI:

1. Acesse http://localhost:8000/docs
2. Clique no botão **"Authorize"** no topo da página
3. Primeiro, registre um usuário usando `POST /api/v1/auth/register`
4. Use o `access_token` retornado no campo de autorização
5. Clique em "Authorize" e depois "Close"
6. Agora você pode testar todos os endpoints protegidos!

---

### Verificar Status da API (Público - Sem Autenticação)

**Via curl:**
```bash
curl http://localhost:8000/health/
```

**Via Swagger:**
1. Acesse http://localhost:8000/docs
2. Localize `GET /health/`
3. Clique em "Try it out" → "Execute"
4. Visualize a resposta com status da API e conectividade do banco

---

### Registrar Novo Usuário

**Via curl:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

**Resposta de exemplo:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Nota**: O primeiro usuário registrado automaticamente se torna administrador.

---

### Listar Livros (com paginação) - Requer Autenticação

**Via curl:**
```bash
# Substitua SEU_TOKEN pelo access_token obtido no registro/login
curl "http://localhost:8000/books/?page=1&per_page=10" \
  -H "Authorization: Bearer SEU_TOKEN"
```

**Via Swagger:**
1. Acesse http://localhost:8000/docs
2. **Clique em "Authorize"** e insira seu token
3. Localize `GET /books/`
4. Clique em "Try it out"
5. Ajuste os parâmetros:
   - `page`: 1
   - `per_page`: 10
6. Clique em "Execute"

**Resposta de exemplo:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "A Light in the Attic",
      "price": "51.77",
      "rating": 3,
      "availability": true,
      "category": "Poetry",
      "image": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
    }
  ],
  "page": 1,
  "per_page": 10,
  "total": 100,
  "pages": 10,
  "next": "http://localhost:8000/books/?page=2&per_page=10",
  "previous": null
}
```

---

### Buscar Livro por ID - Requer Autenticação

**Via curl:**
```bash
curl "http://localhost:8000/books/1" \
  -H "Authorization: Bearer SEU_TOKEN"
```

**Via Swagger:**
1. Acesse http://localhost:8000/docs
2. **Certifique-se de estar autenticado** (botão "Authorize")
3. Localize `GET /books/{id}`
4. Clique em "Try it out"
5. Insira o `id` desejado (ex: 1)
6. Clique em "Execute"

**Resposta de exemplo:**
```json
{
  "id": 1,
  "title": "A Light in the Attic",
  "price": "51.77",
  "rating": 3,
  "availability": true,
  "category": "Poetry",
  "image": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
}
```

---

### Buscar Livros por Título

**Via curl:**
```bash
curl "http://localhost:8000/books/search?title=python&page=1&per_page=10"
```

**Via Swagger:**
1. Acesse http://localhost:8000/docs
2. Localize `GET /books/search`
3. Clique em "Try it out"
4. Preencha os parâmetros:
   - `title`: "python"
   - `page`: 1
   - `per_page`: 10
5. Clique em "Execute"

**Resposta de exemplo:**
```json
{
  "data": [
    {
      "id": 23,
      "title": "Learning Python",
      "price": "30.23",
      "rating": 4,
      "availability": true,
      "category": "Programming",
      "image": "https://books.toscrape.com/media/cache/..."
    }
  ],
  "page": 1,
  "per_page": 10,
  "total": 15,
  "pages": 2,
  "next": "http://localhost:8000/books/search?title=python&per_page=10&page=2",
  "previous": null
}
```

---

### Buscar Livros por Categoria

**Via curl:**
```bash
curl "http://localhost:8000/books/search?category=Fiction&page=1&per_page=10"
```

**Via Swagger:**
1. Acesse http://localhost:8000/docs
2. Localize `GET /books/search`
3. Clique em "Try it out"
4. Preencha:
   - `category`: "Fiction"
   - `page`: 1
   - `per_page`: 10
5. Clique em "Execute"

---

### Listar Todas as Categorias

**Via curl:**
```bash
curl "http://localhost:8000/categories/?page=1&per_page=20"
```

**Via Swagger:**
1. Acesse http://localhost:8000/docs
2. Localize `GET /categories/`
3. Clique em "Try it out"
4. Ajuste:
   - `page`: 1
   - `per_page`: 20
5. Clique em "Execute"

**Resposta de exemplo:**
```json
{
  "data": [
    {"name": "Travel", "count": 11},
    {"name": "Mystery", "count": 32},
    {"name": "Historical Fiction", "count": 14}
  ],
  "page": 1,
  "per_page": 20,
  "total": 50,
  "pages": 3,
  "next": "http://localhost:8000/categories/?page=2&per_page=20",
  "previous": null
}
```

---

### Disparar Processo de Scraping - Requer Admin

**IMPORTANTE**: Este endpoint requer privilégios de administrador. Apenas o primeiro usuário registrado ou usuários com flag `is_admin=true` podem acessá-lo.

**Via curl:**
```bash
# Requer token de usuário ADMIN
curl -X POST http://localhost:8000/scraping/trigger \
  -H "Authorization: Bearer TOKEN_DO_ADMIN"
```

**Via Swagger:**
1. Acesse http://localhost:8000/docs
2. **Autentique com usuário admin** (primeiro usuário registrado)
3. Localize `POST /scraping/trigger`
4. Clique em "Try it out"
5. Clique em "Execute"
6. Aguarde o processo concluir (pode levar alguns minutos)

**Resposta de exemplo:**
```json
{
  "status": "completed",
  "total_books": 1000,
  "total_categories": 50,
  "csv_file": "data/books.csv",
  "execution_time": "45.2s"
}
```

---

### Verificar Status do Scraping

**Via curl:**
```bash
curl "http://localhost:8000/scraping/status"
```

**Via Swagger:**
1. Acesse http://localhost:8000/docs
2. Localize `GET /scraping/status`
3. Clique em "Try it out" → "Execute"

**Resposta de exemplo:**
```json
{
  "total_books": 1000,
  "total_categories": 50,
  "last_updated": "2025-10-21T14:30:00"
}
```

---

### 💡 Dicas para Usar o Swagger UI

- **Schemas**: Role até o final da página do Swagger para ver todos os modelos de dados
- **Validação**: O Swagger valida automaticamente os tipos de dados antes de enviar
- **Exemplos**: Clique em "Schema" ao lado de "Example Value" para ver a estrutura completa
- **Download**: Baixe a especificação OpenAPI em http://localhost:8000/openapi.json
- **Autorização**: Quando implementada autenticação, use o botão "Authorize" no topo

## 📁 Estrutura do Projeto

```
tech-challenge-1/
├── src/
│   ├── api/
│   │   └── schemas/          # Schemas Pydantic para validação
│   │       ├── book.py
│   │       └── auth.py       # Schemas de autenticação
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
│   │   ├── auth/              # Sistema de autenticação
│   │   │   ├── password.py    # Hash e validação de senhas
│   │   │   ├── jwt.py         # Gerenciamento de tokens JWT
│   │   │   └── dependencies.py # Dependências de autenticação
│   │   └── scraping/          # Lógica de web scraping
│   │       ├── core.py        # Scraper assíncrono principal
│   │       └── file_handler.py # Manipulação de arquivos CSV
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

**Tabela: users**
- `id` (Integer, PK) - Identificador único
- `email` (String, unique) - Email do usuário
- `password` (String) - Senha hasheada com Bcrypt
- `is_active` (Boolean) - Usuário ativo
- `is_admin` (Boolean) - Privilégios de administrador
- `created_at` (DateTime) - Data de criação

### Gerenciamento do Banco

O banco de dados é gerenciado via Alembic migrations:

```bash
# Criar o banco e todas as tabelas
uv run alembic upgrade head

# Ver histórico de migrations
uv run alembic history

# Criar nova migration (após alterar models)
uv run alembic revision --autogenerate -m "descrição"
```

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
- ✅ Sistema de autenticação JWT (64 testes)
  - Password hashing e validação
  - Criação e validação de tokens
  - Endpoints de autenticação (registro, login, refresh)
  - Proteção de endpoints
  - Controle de acesso admin

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

## 🔒 Segurança

### Práticas de Segurança Implementadas

1. **Autenticação JWT**
   - Tokens assinados com HMAC SHA-256
   - Tokens de curta duração (10 minutos para access, 5 minutos para refresh)
   - Separação de access e refresh tokens

2. **Senhas**
   - Hash com Bcrypt (algoritmo adaptativo)
   - Validação de força: mínimo 8 caracteres, letras maiúsculas, minúsculas e dígitos
   - Nunca armazenadas em texto plano

3. **Controle de Acesso**
   - Role-Based Access Control (RBAC)
   - Endpoints protegidos por autenticação
   - Endpoints administrativos requerem privilégios especiais
   - Sistema de gerenciamento de admin (promote/demote)
   - Proteção contra auto-rebaixamento (admins não podem se remover)

4. **Validação de Dados**
   - Validação via Pydantic em todas as entradas
   - Sanitização automática de dados
   - Tipos de dados fortemente tipados

### Recomendações de Produção

Para ambiente de produção, recomenda-se:
- [ ] Usar HTTPS (TLS/SSL)
- [ ] Configurar CORS apropriadamente
- [ ] Implementar rate limiting
- [ ] Adicionar logging de segurança
- [ ] Usar SECRET_KEY gerada criptograficamente
- [ ] Implementar rotação de tokens
- [ ] Adicionar autenticação de dois fatores (2FA)
- [ ] Configurar timeouts de sessão
- [ ] Implementar proteção contra CSRF

## 🎓 Cenário de Uso para ML

Esta API foi desenvolvida pensando em servir como base para:
1. **Sistemas de Recomendação**: Dados estruturados de livros, categorias e ratings
2. **Análise de Preços**: Histórico e comparação de preços
3. **Classificação de Texto**: Categorização automática baseada em títulos
4. **Feature Engineering**: Endpoints preparados para exportar features
5. **Controle de Acesso**: Sistema de autenticação pronto para integração com serviços ML

## 👥 Equipe

Desenvolvido como parte do Tech Challenge - Fase 1
Pós-Tech FIAP - Machine Learning Engineering

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Observação**: Este projeto foi desenvolvido para fins educacionais como parte do Tech Challenge da FIAP.
