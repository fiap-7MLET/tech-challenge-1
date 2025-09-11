from flask import Flask

from flask import Flask
from extensions import db
from conf import Conf
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Conf)

    db.init_app(app)
    register_blueprints(app)

    return app

if __name__ == '__main__':
    from alembic import command
    from alembic.config import Config

    app = create_app()

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    app.run(host='0.0.0.0', port=5000, debug=True)

