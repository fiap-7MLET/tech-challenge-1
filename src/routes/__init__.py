from .user_routes import user_bp
from .book_routes import book_bp
from .health_routes import health_bp
from .category_routes import category_bp

def register_blueprints(app):
    prefix = app.config["V1_ROOT"]
    app.register_blueprint(user_bp, url_prefix=f"{prefix}/auth", strict_slashes=False)
    app.register_blueprint(book_bp, url_prefix=f"{prefix}/books", strict_slashes=False)
    app.register_blueprint(health_bp, url_prefix=f"{prefix}/health", strict_slashes=False)
    app.register_blueprint(category_bp, url_prefix=f"{prefix}/categories", strict_slashes=False)
