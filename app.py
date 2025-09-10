from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

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

    main_app = Flask(__name__)
    v1_app = create_app()

    application = DispatcherMiddleware(main_app.wsgi_app, {
        Conf.V1_ROOT: v1_app
    })

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    app = create_app()
    run_simple("0.0.0.0", 5000, application, use_debugger=True, use_reloader=True)

