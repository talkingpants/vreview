from flask import Blueprint, jsonify, request, Response
import csv
import io
from . import db
from .models import Vulnerability, Review, Ticket
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


# -------------------------- Vulnerability CRUD ---------------------------

@api_bp.route('/vulnerabilities', methods=['GET'])
def list_vulnerabilities():
    vulnerabilities = Vulnerability.query.all()
    return jsonify([v.to_dict() for v in vulnerabilities])


@api_bp.route('/vulnerabilities/<int:vuln_id>', methods=['GET'])
def get_vulnerability(vuln_id):
    vulnerability = Vulnerability.query.get(vuln_id)
    if not vulnerability:
        return jsonify({'error': 'Vulnerability not found'}), 404
    return jsonify(vulnerability.to_dict())


@api_bp.route('/vulnerabilities', methods=['POST'])
def create_vulnerability():
    data = request.get_json() or {}
    try:
        vulnerability = Vulnerability(
            defender_id=data['defender_id'],
            title=data['title'],
            description=data.get('description'),
            severity=data.get('severity'),
        )
        db.session.add(vulnerability)
        db.session.commit()
        return jsonify(vulnerability.to_dict()), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/vulnerabilities/<int:vuln_id>', methods=['PUT'])
def update_vulnerability(vuln_id):
    vulnerability = Vulnerability.query.get(vuln_id)
    if not vulnerability:
        return jsonify({'error': 'Vulnerability not found'}), 404
    data = request.get_json() or {}
    for field in ['defender_id', 'title', 'description', 'severity']:
        if field in data:
            setattr(vulnerability, field, data[field])
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    return jsonify(vulnerability.to_dict())


@api_bp.route('/vulnerabilities/<int:vuln_id>', methods=['DELETE'])
def delete_vulnerability(vuln_id):
    vulnerability = Vulnerability.query.get(vuln_id)
    if not vulnerability:
        return jsonify({'error': 'Vulnerability not found'}), 404
    try:
        db.session.delete(vulnerability)
        db.session.commit()
        return jsonify({'message': 'Vulnerability deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ----------------------------- Review CRUD ------------------------------

@api_bp.route('/reviews', methods=['GET'])
def list_reviews():
    reviews = Review.query.all()
    return jsonify([r.to_dict() for r in reviews])


@api_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    return jsonify(review.to_dict())


@api_bp.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json() or {}
    try:
        review = Review(
            vulnerability_id=data['vulnerability_id'],
            status=data.get('status', 'pending'),
            comments=data.get('comments'),
            reviewed_at=data.get('reviewed_at'),
        )
        db.session.add(review)
        db.session.commit()
        return jsonify(review.to_dict()), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    data = request.get_json() or {}
    for field in ['vulnerability_id', 'status', 'comments', 'reviewed_at']:
        if field in data:
            setattr(review, field, data[field])
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    return jsonify(review.to_dict())


@api_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    try:
        db.session.delete(review)
        db.session.commit()
        return jsonify({'message': 'Review deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ------------------------------ Ticket CRUD -----------------------------

@api_bp.route('/tickets', methods=['GET'])
def list_tickets():
    tickets = Ticket.query.all()
    return jsonify([t.to_dict() for t in tickets])


@api_bp.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    return jsonify(ticket.to_dict())


@api_bp.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json() or {}
    try:
        ticket = Ticket(
            review_id=data['review_id'],
            ticket_number=data.get('ticket_number'),
            status=data.get('status', 'open'),
        )
        db.session.add(ticket)
        db.session.commit()
        return jsonify(ticket.to_dict()), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    data = request.get_json() or {}
    for field in ['review_id', 'ticket_number', 'status']:
        if field in data:
            setattr(ticket, field, data[field])
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    return jsonify(ticket.to_dict())


@api_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    try:
        db.session.delete(ticket)
        db.session.commit()
        return jsonify({'message': 'Ticket deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ----------------------------------------------------------------------
# Helper route: create a review and ticket from a vulnerability ID
# ----------------------------------------------------------------------
@api_bp.route('/tickets/from-vulnerability', methods=['POST'])
def create_ticket_from_vulnerability():
    """Create a ticket and review for a given vulnerability."""
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

    return jsonify({
        "id": ticket.id,
        "ticket_number": ticket.ticket_number,
        "status": ticket.status,
    }), 201


# ---------------------------- Utility Actions ----------------------------

@api_bp.route('/sync-defender', methods=['POST'])
def sync_defender_route():
    """Pull vulnerable software from Defender and store/update records."""
    try:
        data = get_vulnerable_software()
        items = data.get('value', data)
        created = 0
        for item in items:
            if not isinstance(item, dict):
                continue
            defender_id = item.get('id') or item.get('productId')
            title = item.get('name') or item.get('title')
            severity = item.get('severity')
            if not defender_id or not title:
                continue
            vuln = Vulnerability.query.filter_by(defender_id=defender_id).first()
            if vuln:
                vuln.title = title
                vuln.severity = severity
            else:
                vuln = Vulnerability(defender_id=defender_id, title=title, severity=severity)
                db.session.add(vuln)
                created += 1
        db.session.commit()
        return jsonify({'created': created})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/vulnerabilities/clear', methods=['POST'])
def clear_vulnerabilities():
    """Delete all cached vulnerabilities."""
    try:
        count = Vulnerability.query.delete()
        db.session.commit()
        return jsonify({'cleared': count})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/vulnerabilities/export', methods=['GET'])
def export_vulnerabilities():
    fmt = request.args.get('format', 'json')
    vulns = Vulnerability.query.all()
    if fmt == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['id', 'defender_id', 'title', 'severity'])
        for v in vulns:
            writer.writerow([v.id, v.defender_id, v.title, v.severity])
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=vulnerabilities.csv'}
        )
    else:
        return jsonify([v.to_dict() for v in vulns])


@api_bp.route('/settings', methods=['POST'])
def save_settings():
    """Placeholder endpoint to accept settings."""
    data = request.get_json() or {}
    # Settings persistence not implemented; just acknowledge receipt
    return jsonify({'saved': True, 'received': data})


@api_bp.route('/verify-defender', methods=['POST'])
def verify_defender():
    """Verify Microsoft Defender credentials by attempting authentication."""
    data = request.get_json() or {}
    tenant = data.get('tenant_id')
    client = data.get('client_id')
    secret = data.get('client_secret')
    try:
        get_access_token(tenant, client, secret)
        return jsonify({'valid': True})
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 400
