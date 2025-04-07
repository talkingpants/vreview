from flask import Blueprint, jsonify

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__)

# Root route to test if the API is running
@api_bp.route('/', methods=['GET'])
def root():
    return jsonify({"message": "Welcome to the Flask API root!"})

# Simple hello route
@api_bp.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask!"})
