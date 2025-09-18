
"""
Extensões de banco de dados para uso com FastAPI e SQLAlchemy puro.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependência do FastAPI para obter a sessão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
