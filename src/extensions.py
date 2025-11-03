"""Configuração e gerenciamento de conexão com o banco de dados."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def get_db():
    """
    Dependency para obter uma sessão do banco de dados.

    Yields:
            Session: Sessão do banco de dados que será fechada automaticamente
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
