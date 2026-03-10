import requests
from utils.config import BASE_URL, USERNAME, PASSWORD

def get_auth_token_from_login():
    """
    Logs in to the API and returns the auth_token from cookies.
    Raises Exception if not found.
    """
    login_url = f"{BASE_URL}/tools/api/login/"
    payload = {"username": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/json"}
    session = requests.Session()
    resp = session.post(login_url, headers=headers, json=payload)
    resp.raise_for_status()
    # Try to get auth_token from session or response cookies
    auth_token = session.cookies.get('auth_token') or resp.cookies.get('auth_token')
    if not auth_token:
        print("DEBUG: Login cookies:", session.cookies)
        print("DEBUG: Login response cookies:", resp.cookies)
        raise Exception("No auth_token found in login cookies")
    return auth_token

# Optionally, add a validation function

def validate_auth_token(token):
    """
    Optionally validate the token by making a simple authenticated request.
    Returns True if valid, False otherwise.
    """
    test_url = f"{BASE_URL}/tools/api/virustotal/report/ip/"
    headers = {
        'Cookie': f'auth_token={token}',
        'Content-Type': 'application/json'
    }
    payload = {"ip": "8.8.8.8"}
    resp = requests.post(test_url, headers=headers, json=payload)
    return resp.status_code == 200
