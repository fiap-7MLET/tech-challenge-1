from src.conf import Conf

def test_conf_constants():
    assert Conf.V1_ROOT == "/api/v1"
    assert "db.sqlite3" in Conf.SQLALCHEMY_DATABASE_URI or Conf.SQLALCHEMY_DATABASE_URI.startswith("sqlite:///")
    assert Conf.SQLALCHEMY_TRACK_MODIFICATIONS is False

def test_auth_constants():
    """Test authentication configuration constants."""
    assert Conf.ALGORITHM == "HS256"
    assert Conf.ACCESS_TOKEN_EXPIRE_MINUTES == 10
    assert Conf.REFRESH_TOKEN_EXPIRE_MINUTES == 5
    assert hasattr(Conf, "SECRET_KEY")
