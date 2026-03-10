import requests
import pytest
from utils.auth_token_helper import get_auth_token_from_login
from utils.config import BASE_URL

def test_mailxray_virustotal_ip_from_csv():
    """Validate virustotal API with IP read from testdata/mailxray_homepage.csv"""
    import csv
    from pathlib import Path
    csv_path = Path(__file__).parent.parent.parent.parent / "testdata" / "mailxray_homepage.csv"
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        ip_value = row.get('IP')
        print(f"Testing with IP: {ip_value}")
    url = f"{BASE_URL}/tools/api/virustotal/report/ip/"
    auth_token = get_auth_token_from_login()
    headers = {
        'Cookie': f'auth_token={auth_token}',
        'Content-Type': 'application/json'
    }
    payload = {"ip": ip_value}
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Response JSON:", response.json())

