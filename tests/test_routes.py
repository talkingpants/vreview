from unittest.mock import patch

from backend.app import db
from backend.app.models import Vulnerability


def test_root_route(client):
    response = client.get('/api/v1/')
    data = response.get_json()
    assert response.status_code == 200
    assert 'message' in data


def test_hello_route(client):
    response = client.get('/api/v1/hello')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello from Flask!"}


def test_vulnerable_software_route(client):
    sample = {"value": [{"id": "1", "name": "test"}]}
    with patch('backend.app.routes.get_vulnerable_software', return_value=sample):
        response = client.get('/api/v1/vulnerable-software')
    assert response.status_code == 200
    assert response.get_json() == sample


def test_create_ticket_from_vulnerability(client, app):
    with app.app_context():
        vuln = Vulnerability(defender_id='v1', title='Test Vuln')
        db.session.add(vuln)
        db.session.commit()

    resp = client.post(
        '/api/v1/tickets/from-vulnerability',
        json={'vulnerability_id': vuln.id}
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['ticket_number']
    assert data['status'] == 'open'


def test_dashboard_page_served(client):
    resp = client.get('/dashboard.html')
    assert resp.status_code == 200
    assert b'VReview - Dashboard' in resp.data


def test_reviews_page_served(client):
    resp = client.get('/reviews.html')
    assert resp.status_code == 200
    assert b'VReview - Reviews' in resp.data

