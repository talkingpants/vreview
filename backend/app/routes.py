from flask import Blueprint, jsonify
from . import db
from .defender import get_vulnerable_software

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


@api_bp.route('/vulnerable-software', methods=['GET'])
def vulnerable_software():
    """Return list of vulnerable software from Microsoft Defender."""
    try:
        data = get_vulnerable_software()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
