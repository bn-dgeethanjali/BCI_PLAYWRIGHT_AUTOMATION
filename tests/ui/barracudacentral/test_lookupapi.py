import pytest
import requests
import re
import os
from playwright.sync_api import sync_playwright



@pytest.mark.parametrize("ip, expected_return_code, expected_message", [
    ("0.0.0.0", 0, "The IP address 0.0.0.0 is not currently listed as poor on the Barracuda Reputation System."),("72.211.30.216", 1, "The IP address 72.211.30.216 is listed as poor on the Barracuda Reputation System."),
    # Add more test cases here as needed
])

def test_lookup_ip(ip, expected_return_code, expected_message):
    
    url = os.getenv("BARRACUDA_API_URL", "https://barracudacentral.barracudabrts.com/api/v1/lookup/ip")
    params = {"ip": ip}
    headers = {
        "x-api-key": os.getenv("BARRACUDA_API_KEY", "barracuda_4f8e2c7a-9b1e-4e2a-8c3d-7f6a2b1c9e5d"),
        "Accept": os.getenv("BARRACUDA_API_ACCEPT", "application/json")
    }
    print("******************lookup*******",url,headers)
    response = requests.get(url, params=params, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    print(response.text)
    current_BCR = barracuda_central_lookup(ip=ip)
    print("Current BCR from Playwright:", current_BCR)
    assert data["ip"] == ip
    assert data["returnCode"] == expected_return_code
    assert data["message"] == expected_message
    assert data["message"] == current_BCR

def barracuda_central_lookup(ip):
    url = "https://barracudacentral.org/lookups"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector('input#ir_entry')
        page.fill('input#ir_entry', ip)
        page.click('input[type=\"submit\"]')
        try:
            response_text = page.inner_text('.lookup-result')
        except Exception:
            try:
                response_text = page.inner_text('.result')
            except Exception:
                response_text = page.inner_text('body')
        
        #Accept both with and without quotes around 'poor' for robustness
        pattern_with_quotes = rf'The IP address {re.escape(ip)} is listed as "poor" on the Barracuda Reputation System.'
        pattern_without_quotes = rf'The IP address {re.escape(ip)} is listed as poor on the Barracuda Reputation System.'
        match = re.search(pattern_with_quotes, response_text)
        if match:
            filtered_text = match.group(0).replace('"poor"', 'poor')
        else:
            match = re.search(pattern_without_quotes, response_text)
            if match:
                filtered_text = match.group(0)
            else:
                filtered_text = f'The IP address {ip} is not currently listed as poor on the Barracuda Reputation System.'
        print(filtered_text)
        browser.close()
        return filtered_text
    
#export BARRACUDA_API_URL="http://barracudacentral.dev.bci.aws.cudaops.com/api/v1/lookup/ip"
#export BARRACUDA_API_KEY="barracuda_4f8e2c7a-9b1e-4e2a-8c3d-7f6a2b1c9e5d"
#export BARRACUDA_API_ACCEPT="application/json"
#pytest -v -s tests/test_lookupapi.py
#Exec:pytest -v -s tests/test_lookupapi_p.py --junitxml=tests/reports/junit-results.xml# This file was moved from playwrite-automation-app/automation_app/tests/test_lookupapi_copy.py
# Place your UI test code here.

# ...existing code from test_lookupapi_copy.py...