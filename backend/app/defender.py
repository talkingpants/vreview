import os
import json
import requests

from . import db
from .models import Vulnerability


def get_access_token():
    tenant_id = os.getenv("DEFENDER_TENANT_ID")
    client_id = os.getenv("DEFENDER_CLIENT_ID")
    client_secret = os.getenv("DEFENDER_CLIENT_SECRET")
    if not all([tenant_id, client_id, client_secret]):
        raise RuntimeError("Defender API credentials are not fully configured")

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://api.securitycenter.microsoft.com/.default",
        "grant_type": "client_credentials",
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    return response.json().get("access_token")


def get_vulnerable_software():
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    url = "https://api.securitycenter.microsoft.com/api/vulnerableSoftware"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def sync_vulnerabilities():
    """Fetch vulnerable software from Defender API and store in the DB."""
    data = get_vulnerable_software()
    # Defender API typically returns a {"value": [...]} object
    items = data.get("value") if isinstance(data, dict) else data
    if items is None:
        return 0

    created = 0
    for item in items:
        defender_id = str(
            item.get("id")
            or item.get("cveId")
            or item.get("softwareId")
        )
        if not defender_id:
            continue

        vulnerability = Vulnerability.query.filter_by(defender_id=defender_id).first()
        if vulnerability is None:
            vulnerability = Vulnerability(defender_id=defender_id)
            created += 1

        vulnerability.title = (
            item.get("name")
            or item.get("softwareName")
            or item.get("title")
            or defender_id
        )
        vulnerability.description = item.get("description") or json.dumps(item)
        vulnerability.severity = item.get("severity") or item.get("highestSeverity")

        db.session.add(vulnerability)

    db.session.commit()
    return created
