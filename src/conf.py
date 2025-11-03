import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Conf:
    V1_ROOT = "/api/v1"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'db', 'dbzao.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
