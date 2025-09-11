from .user_routes import user_bp

def register_blueprints(app):
    prefix = app.config["V1_ROOT"]
    app.register_blueprint(user_bp, url_prefix=f"{prefix}/auth")
