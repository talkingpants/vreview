from flask import Blueprint, jsonify
from . import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET'])
def root():
    try:
        with db.engine.connect() as conn:
            result = conn.execute("SELECT 1")
            return jsonify({"message": "DB connected!", "result": result.scalar()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask!"})
