import os
from datetime import timedelta

# Project root directory (parent of src/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Conf:
    V1_ROOT = "/api/v1"
    # Use DATABASE_URL from environment or default to root db.sqlite3
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(PROJECT_ROOT, 'db.sqlite3')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Authentication settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 10
    REFRESH_TOKEN_EXPIRE_MINUTES = 5
