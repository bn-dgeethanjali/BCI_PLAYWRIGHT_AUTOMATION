import requests
import pytest
from utils.auth_token_helper import get_auth_token_from_login

def test_phaas_evilproxy_scan():
    """Test PHaaS API with Evilproxy HTML and validate response structure and values."""
    # Get auth token
    auth_token = get_auth_token_from_login()
    url = "https://mailxray.barracudabrts.com/tools/api/phaas/"
    headers = {
        'Cookie': f'auth_token={auth_token}'
    }
    # Read HTML file from testdata
    html_path = "testdata/Evilproxy_06_01_2026.html"
    with open(html_path, 'rb') as f:
        files = {'html': ("flowerstorm_match_example.html", f, 'text/html')}
        data = {
            'scan_with_yara': 'true',
            'calculate_hashes': 'true'
        }
        response = requests.post(url, headers=headers, files=files, data=data)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    resp_json = response.json()
    assert resp_json.get("message") == "PHAAS scan completed successfully"
    data = resp_json.get("data", {})
    # Validate hashes (actual values from API)
    hashes = data.get("hashes", {})
    assert hashes.get("md5") == "fcebd24373974990f63a5610336c4b46"
    assert hashes.get("sha1") == "f43c57f2023cefc0d5d3dcaf4a33410806e19010"
    assert hashes.get("sha256") == "f44df2df476be68020a46470a18d49bec925d798a030b7f2db39d6750258a8c9"
    # Validate yara_matches
    yara_matches = data.get("yara_matches", {})
    # Validate Evilginx2_Comments
    evilginx = yara_matches.get("Evilginx2_Comments", {})
    evilginx_meta = evilginx.get("meta", {})
    assert evilginx_meta.get("description") == "Evilginx2 Phaas detection"
    # Validate Tycoon_Obfuscation_01
    tycoon = yara_matches.get("Tycoon_Obfuscation_01", {})
    tycoon_meta = tycoon.get("meta", {})
    assert tycoon_meta.get("description") == "Tycoon 2FA phishing kit"
    # ...existing code...
