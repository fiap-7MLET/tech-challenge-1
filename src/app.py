from flask import Flask
from pathlib import Path

from extensions import db
from conf import Conf
from routes import register_blueprints
from services.scraping.core import scrape_all_books
from services.scraping.file_handler import update_books_data


def create_app(config_object=Conf):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    db.init_app(app)
    register_blueprints(app)

    # Provisoriamente chamado aqui para garantir que o arquivo CSV exista
    with app.app_context():
        project_root = Path(__file__).parent.parent
        output_file = project_root / "data" / "scraped_books.csv"
        if not output_file.exists():
            update_books_data(output_file, scraper_function=scrape_all_books)

    return app

if __name__ == '__main__':
    from alembic import command
    from alembic.config import Config

    app = create_app()

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    app.run(host='0.0.0.0', port=5000, debug=True)

