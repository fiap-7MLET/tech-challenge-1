from src.conf import Conf


def test_conf_constants():
    assert Conf.V1_ROOT == "/api/v1"
    assert Conf.SQLALCHEMY_DATABASE_URI.endswith("dbzao.db")
    assert Conf.SQLALCHEMY_TRACK_MODIFICATIONS is False
