from unittest.mock import patch

from backend.app import db
from backend.app.models import Vulnerability


def test_root_route(client):
    response = client.get('/api/v1/')
    data = response.get_json()
    assert response.status_code == 200
    assert 'message' in data


def test_index_page_served(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Stored Vulnerabilities' in resp.data


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


def test_sync_defender_creates_vulnerability(client, app):
    sample = {"value": [{"id": "abc", "name": "Foo", "severity": "Medium"}]}
    with patch('backend.app.routes.get_vulnerable_software', return_value=sample):
        resp = client.post('/api/v1/sync-defender')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['created'] == 1
    with app.app_context():
        vuln = Vulnerability.query.filter_by(defender_id='abc').first()
        assert vuln is not None
        assert vuln.title == 'Foo'
        assert vuln.severity == 'Medium'


def test_clear_vulnerabilities(client, app):
    with app.app_context():
        db.session.add(Vulnerability(defender_id='1', title='A'))
        db.session.add(Vulnerability(defender_id='2', title='B'))
        db.session.commit()

    resp = client.post('/api/v1/vulnerabilities/clear')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['cleared'] == 2
    with app.app_context():
        assert Vulnerability.query.count() == 0


def test_settings_post(client):
    payload = {"theme": "dark"}
    resp = client.post('/api/v1/settings', json=payload)
    assert resp.status_code == 200
    assert resp.get_json() == {'saved': True, 'received': payload}


def test_export_vulnerabilities_csv(client, app):
    with app.app_context():
        vuln = Vulnerability(defender_id='v1', title='Test Vuln', severity='High')
        db.session.add(vuln)
        db.session.commit()
        vuln_id = vuln.id

    resp = client.get('/api/v1/vulnerabilities/export?format=csv')
    assert resp.status_code == 200
    assert resp.mimetype == 'text/csv'
    assert 'filename=vulnerabilities.csv' in resp.headers.get('Content-Disposition', '')
    csv_text = resp.get_data(as_text=True)
    assert 'id,defender_id,title,severity' in csv_text
    assert f"{vuln_id},v1,Test Vuln,High" in csv_text


def test_verify_defender_success(client):
    with patch('backend.app.routes.get_access_token', return_value='tok'):
        resp = client.post('/api/v1/verify-defender', json={
            'tenant_id': 't',
            'client_id': 'c',
            'client_secret': 's'
        })
    assert resp.status_code == 200
    assert resp.get_json() == {'valid': True}


def test_verify_defender_failure(client):
    with patch('backend.app.routes.get_access_token', side_effect=RuntimeError('bad')):
        resp = client.post('/api/v1/verify-defender', json={
            'tenant_id': 't',
            'client_id': 'c',
            'client_secret': 's'
        })
    assert resp.status_code == 400
    data = resp.get_json()
    assert data['valid'] is False
    assert 'error' in data

