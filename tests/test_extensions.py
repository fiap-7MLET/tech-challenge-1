import os
import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session
import src.extensions as extensions

def test_database_url_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    # Reload dotenv and extensions to pick up the new env
    import importlib
    importlib.reload(extensions)
    assert os.getenv("DATABASE_URL") == "sqlite:///:memory:"

def test_engine_instance():
    assert isinstance(extensions.engine, Engine)

def test_sessionlocal_instance():
    assert isinstance(extensions.SessionLocal, scoped_session)
