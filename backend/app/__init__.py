import os
from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from .config import Config

# Load environment variables by searching for a `.env` file in the following
# order:
# 1) `../.env`   - when the file lives next to the `backend` package (Docker)
# 2) `../../.env` - at the repository root when running locally
# If neither exists, fall back to the default `load_dotenv()` behaviour which
# looks for a `.env` in the current working directory.
base_dir = os.path.dirname(__file__)
env_candidates = [
    os.path.join(base_dir, '../.env'),
    os.path.join(base_dir, '../../.env'),
]
for env in env_candidates:
    if os.path.exists(env):
        load_dotenv(dotenv_path=env)
        break
else:
    load_dotenv()

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
