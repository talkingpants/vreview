from flask import Blueprint, jsonify, request
from . import db
from .defender import get_vulnerable_software
from .models import Vulnerability, Review, Ticket

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET'])
def root():
    try:
        with db.engine.connect() as conn:
            result = conn.execute("SELECT 1")
            return jsonify({"message": "DB connected!", "result": result.scalar()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route('/vulnerabilities', methods=['GET'])
def list_vulnerabilities():
    """Return vulnerabilities stored in the database."""
    vulns = Vulnerability.query.all()
    result = [
        {
            "id": v.id,
            "defender_id": v.defender_id,
            "title": v.title,
            "description": v.description,
            "severity": v.severity,
        }
        for v in vulns
    ]
    return jsonify(result)


@api_bp.route('/tickets', methods=['POST'])
def create_ticket():
    """Create a ticket for a given vulnerability."""
    data = request.get_json() or {}
    vuln_id = data.get("vulnerability_id")
    if not vuln_id:
        return jsonify({"error": "vulnerability_id is required"}), 400

    vulnerability = Vulnerability.query.get(vuln_id)
    if not vulnerability:
        return jsonify({"error": "vulnerability not found"}), 404

    review = Review(vulnerability_id=vulnerability.id, status="pending")
    db.session.add(review)
    db.session.commit()

    ticket_number = data.get("ticket_number") or f"TICKET-{review.id}"
    ticket = Ticket(review_id=review.id, ticket_number=ticket_number)
    db.session.add(ticket)
    db.session.commit()

    return (
        jsonify({"id": ticket.id, "ticket_number": ticket.ticket_number, "status": ticket.status}),
        201,
    )

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
