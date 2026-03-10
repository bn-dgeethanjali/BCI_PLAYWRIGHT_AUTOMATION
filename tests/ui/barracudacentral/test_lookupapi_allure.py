#/Users/dgeethanjali/AWS/pytest-project/xray_sample_project/brts-automation
import pytest
import requests
import re
import os
import allure
import csv
from playwright.sync_api import sync_playwright



@allure.epic("Barracuda Reputation System")
@allure.feature("IP Reputation Lookup")
@allure.story("Validate IP reputation via API and Web Scraping")




def load_test_data_from_csv():
    import glob
    test_cases = []
    # Directly use absolute path to bci_automation/testdata
    testdata_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../testdata'))
    csv_files = glob.glob(os.path.join(testdata_dir, 'user_*.csv'))
    print("CSV files found:", csv_files)
    for csv_path in csv_files:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ip = (row.get('ip') or '').strip()
                if not ip:
                    continue  # Skip rows with empty IP
                try:
                    expected_return_code = int(row.get('expected_return_code', 0))
                except Exception:
                    expected_return_code = 0
                expected_message = row.get('expected_message', '')
                url = row.get('url', '')
                x_api_key = row.get('x_api_key', '')
                accept = row.get('accept', '')
                test_cases.append((ip, expected_return_code, expected_message, url, x_api_key, accept))
    print("Loaded test cases:", test_cases)
    return test_cases

@pytest.mark.parametrize("ip, expected_return_code, expected_message, url, x_api_key, accept", load_test_data_from_csv())
def test_lookup_ip(ip, expected_return_code, expected_message, url, x_api_key, accept):

    with allure.step(f"Testing IP reputation for: {ip}"):
        allure.attach(ip, name="Test IP Address", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Query Barracuda API for IP reputation"):
            params = {"ip": ip}
            headers = {
                "x-api-key": x_api_key,
                "Accept": accept
            }
            response = requests.get(url, params=params, headers=headers)
            assert response.status_code == 200
            data = response.json()
            allure.attach(str(data), name="API Response", attachment_type=allure.attachment_type.JSON)
            print(response.text)

        with allure.step("Scrape Barracuda website for IP reputation"):
            current_BCR = barracuda_central_lookup(ip=ip)
            allure.attach(current_BCR, name="Web Scraping Result", attachment_type=allure.attachment_type.TEXT)
            print("Current BCR from Playwright:", current_BCR)

        with allure.step("Validate API response data"):
            assert data["ip"] == ip
            assert data["returnCode"] == expected_return_code
            assert data["message"] == expected_message

        with allure.step("Compare API and Web scraping results"):
            assert data["message"] == current_BCR, f"Mismatch: API='{data['message']}', Web='{current_BCR}'"

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
#Exec:pytest -v -s tests/test_lookupapi_p.py --junitxml=tests/reports/junit-results.xml
#/Users/dgeethanjali/AWS/pytest-project/xray_sample_project/brts-automation/.venv/bin/python -m pytest -v -s tests/ui/test_lookupapi_allure.py --alluredir=allure-results
#pytest tests/test_lookupapi.py --alluredir=allure-results -v -s
#allure generate allure-results -o allure-report --clean
#allure serve allure-results
