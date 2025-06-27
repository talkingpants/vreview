import os
from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from .config import Config

# Load .env file. Prefer repository root `.env` as documented in README
# so running the app outside of Docker picks up local configuration.
root_env = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path=root_env)

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    # Serve static files (HTML frontend) from the root URL so that
    # paths like `/dashboard.html` work without an extra `/static` prefix.
    app = Flask(__name__, static_folder="static", static_url_path="")
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register your API routes
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    return app
