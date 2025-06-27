from backend.app import db
from backend.app.models import Vulnerability, Review, Ticket


def test_ticket_model_defaults(app):
    with app.app_context():
        vuln = Vulnerability(defender_id='v1', title='test', description='desc', severity='High')
        db.session.add(vuln)
        db.session.commit()

        review = Review(vulnerability_id=vuln.id)
        db.session.add(review)
        db.session.commit()

        ticket = Ticket(review_id=review.id, ticket_number='SDP-1')
        db.session.add(ticket)
        db.session.commit()

        assert ticket.status == 'open'
        assert 'SDP-1' in repr(ticket)
