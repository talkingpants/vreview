import os
import requests


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
