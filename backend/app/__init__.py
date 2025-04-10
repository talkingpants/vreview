import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env from backend/.env explicitly
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load config from .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default-secret")

    # Enable CORS for frontend integration
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register your API routes
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app
