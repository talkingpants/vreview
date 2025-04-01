from flask import Flask
from flask_cors import CORS
from .routes import api_bp
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    return app
