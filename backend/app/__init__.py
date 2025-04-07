import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env file before anything else
load_dotenv()

# Initialize extensions
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Config from environment
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Enable CORS for frontend integration
    CORS(app)

    # Initialize extensions with app
    db.init_app(app)

    # Import and register API routes
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app
