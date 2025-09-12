from .user_routes import user_bp
from .book_routes import book_bp

def register_blueprints(app):
    prefix = app.config["V1_ROOT"]
    app.register_blueprint(user_bp, url_prefix=f"{prefix}/auth")
    app.register_blueprint(book_bp, url_prefix=f"{prefix}/books")
