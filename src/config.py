"""
Módulo de configuração para a aplicação FastAPI.
Utilize variáveis de ambiente para definir parâmetros sensíveis.
"""
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
DEBUG = os.getenv("DEBUG", "False") == "True"
APP_TITLE = os.getenv("APP_TITLE", "Tech Challenge 1 - FastAPI")
