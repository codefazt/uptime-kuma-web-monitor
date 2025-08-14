from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .routes import auth_routes, token_routes
        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(token_routes.bp)

        @app.route("/")
        def index():
            return redirect(url_for('auth_routes.login'))

    return app
