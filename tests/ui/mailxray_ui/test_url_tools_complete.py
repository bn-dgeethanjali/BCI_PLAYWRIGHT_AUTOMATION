


import sys
import os
import csv
import pytest
from pages.locators.url_tools_locators import URLToolsLocators

# Add workspace root to path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from utils.url_tools import URLToolsPage
from utils.home_page import HomePage
from utils.config import BASE_URL, USERNAME, PASSWORD


def read_homepage_csv():
    """Read test data from mailxray_homepage.csv."""
    csv_path = os.path.join(workspace_root, "testdata", "mailxray_homepage.csv")
    test_data = []
    
    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            test_data.append(row)
    
    return test_data


@pytest.fixture
def authenticated_page(page):
    """Login and return authenticated page."""
    from pages.locators.login_locators import LoginPageLocators
    
    # Navigate and login
    page.goto(BASE_URL)
    page.locator(LoginPageLocators.USERNAME).fill(USERNAME)
    page.locator(LoginPageLocators.PASSWORD).fill(PASSWORD)
    page.locator(LoginPageLocators.LOGIN_BUTTON).click()
    page.wait_for_timeout(2000)
    
    return page


def test_url_tools_complete_flow(authenticated_page):
    """
    Complete URL Tools test flow - all 5 scenarios in one test without refresh.
    Tests: navigation, input visibility, CSV data submission, validation, and multiple submissions.
    """
    csv_data = read_homepage_csv()
    if not csv_data:
        pytest.skip("No CSV data available")
    
    url_tools = URLToolsPage(authenticated_page)
    

    
    # Test 1: Navigate to URL Tools page
    print("\n[Test 1/5] Navigating to URL Tools page...")
    url_tools.navigate()
    authenticated_page.wait_for_timeout(2000)
    assert url_tools.is_on_url_tools_page(), "Not on URL Tools page"
    print("✓ Successfully navigated to URL Tools page")
    
    # Test 2: Verify input field is visible
    print("\n[Test 2/5] Verifying input field visibility...")
    assert url_tools.is_input_visible(), "Input field not visible"
    print("✓ Input field is visible")
    
    # Test 3: Submit URL from CSV
    print("\n[Test 3/5] Submitting URL from CSV...")
    url = csv_data[0].get('URL')
    print(f"  URL: {url}")
    url_tools.submit_url(url)
    #authenticated_page.wait_for_timeout(3000)
    #url_tools = URLToolsPage(authenticated_page)
    #url_tools.navigate()
    authenticated_page.wait_for_timeout(2000)
    # Navigate and validate all tabs
    tab_locators = [
        (URLToolsLocators.URL_UNQUOTE, "URL Unquote"),
        (URLToolsLocators.URL_PROTECT, "URL Protect"),
        (URLToolsLocators.DEFANGED_URL, "Defanged URL"),
        (URLToolsLocators.URL_REDIRECT, "URL Redirect"),
    ]
    for locator, tab_name in tab_locators:
        try:
            print(f"\n[DEBUG] Checking {tab_name} tab with locator: {locator}")
            authenticated_page.wait_for_selector(locator, state="visible", timeout=10000)
            print(f"[DEBUG] {tab_name} tab found, attempting click...")
            authenticated_page.click(locator)
            authenticated_page.wait_for_timeout(1000)
            assert authenticated_page.is_visible(locator), f"{tab_name} tab not visible after click"
            print(f"✓ {tab_name} tab is visible and clickable")
        except Exception as e:
            print(f"✗ {tab_name} tab navigation failed: {e}")
            raise
    
   