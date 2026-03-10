"""
Debug script to inspect homepage elements and test input functionality.
"""
import sys
import os
import csv

# Add workspace root to path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from pages.locators.login_locators import LoginPageLocators
from utils.config import BASE_URL, USERNAME, PASSWORD


def read_testdata_from_csv():
    """Read test data from mailxray_homepage.csv file."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #csv_path = os.path.join(project_root, "testdata", "mailxray_homepage.csv")
    csv_path = os.path.join(workspace_root, "testdata", "mailxray_homepage.csv")
    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)
    return data


def click_virustotal_link(page, idx):
    """Click on VirusTotal link and take screenshot."""
    try:
        virustotal_link = page.locator('a[href="/virustotal"]')
        virustotal_link.wait_for(state="visible", timeout=5000)
        print("\n✓ VirusTotal link found")
        virustotal_link.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        print(f"✓ VirusTotal clicked. Current URL: {page.url}")
        return True
    except Exception as e:
        print(f"✗ VirusTotal link error: {str(e)}")
        return False


def click_mxtoolbox_link(page, idx):
    """Click on MxToolBox link and take screenshot."""
    try:
        mxtoolbox_link = page.locator('a[href*="mxtoolbox"], a:has-text("MxToolBox")')
        mxtoolbox_link.wait_for(state="visible", timeout=5000)
        print("\n✓ MxToolBox link found")
        mxtoolbox_link.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        print(f"✓ MxToolBox clicked. Current URL: {page.url}")
        return True
    except Exception as e:
        print(f"✗ MxToolBox link error: {str(e)}")
        return False


def click_whois_link(page, idx):
    """Click on Who is link and take screenshot."""
    try:
        whois_link = page.locator('a[href*="whois"], a:has-text("Who is")')
        whois_link.wait_for(state="visible", timeout=5000)
        print("\n✓ Who is link found")
        whois_link.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        print(f"✓ Who is clicked. Current URL: {page.url}")
        return True
    except Exception as e:
        print(f"✗ Who is link error: {str(e)}")
        return False


def submit_and_test_links(page, search_input, value, idx, input_type="URL"):
    """Submit input value and test all external links (VirusTotal, MxToolBox, Who is)."""
    print(f"\nTesting {input_type}: {value}")
    search_input.clear()
    page.wait_for_timeout(500)
    search_input.fill(value)
    page.wait_for_timeout(1000)
    
    # Verify input
    input_value = search_input.input_value()
    assert input_value == value, f"Expected: {value}, Got: {input_value}"
    print(f"✓ {input_type} input successful: {value}")
    
    # Press Enter to submit
    print("\nPressing Enter to submit...")
    search_input.press('Enter')
    
    # Wait for results/links to load
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    print(f"✓ Submit successful. Current URL: {page.url}")
    
    # Click on VirusTotal link
    click_virustotal_link(page, idx)
    
    # Click on MxToolBox link
    click_mxtoolbox_link(page, idx)
    
    # Click on Who is link
    click_whois_link(page, idx)


def test_mailxray_homepage_input(page):
    """Test inputting URL, IP, Domain, and Hash into MailXray homepage from CSV data."""
    
    # Login first
    page.goto(BASE_URL)
    
    # Wait for login page to load
    page.wait_for_load_state("networkidle")
    page.locator(LoginPageLocators.USERNAME).wait_for(state="visible", timeout=10000)
    
    page.locator(LoginPageLocators.USERNAME).fill(USERNAME)
    page.locator(LoginPageLocators.PASSWORD).fill(PASSWORD)
    page.locator(LoginPageLocators.LOGIN_BUTTON).click()
    
    # Wait for navigation after login
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    
    print(f"\nCurrent URL after login: {page.url}")
    
    # Navigate to homepage
    page.goto(BASE_URL + "/")
    
    # Wait for homepage to fully load
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    
    print(f"Homepage URL: {page.url}")
    
    # Read test data from CSV
    test_data = read_testdata_from_csv()
    print(f"\nLoaded {len(test_data)} rows from CSV")
    
    # Locate the input field by placeholder
    search_input = page.locator('input[placeholder*="URL, IP address, Domain, Hash"]')
    
    # Wait for input field to be visible
    search_input.wait_for(state="visible", timeout=10000)
    print("\nInput field found and visible")
    
    # Test each row of data
    for idx, row in enumerate(test_data):
        print(f"\n=== Testing Row {idx + 1} ===")
        
        url = row.get('URL', '').strip()
        ip = (row.get('IP') or '').strip()
        domain = (row.get('Domain') or '').strip()
        hash_value = (row.get('Hash') or '').strip()
        
        # Test URL input and submit with external links
        if url:
            print(f"\n{'='*50}")
            print(f"Testing URL: {url}")
            print(f"{'='*50}")
            submit_and_test_links(page, search_input, url, idx, input_type="URL")
        
        # Test IP input and submit with external links
        if ip:
            print(f"\n{'='*50}")
            print(f"Testing IP: {ip}")
            print(f"{'='*50}")
            submit_and_test_links(page, search_input, ip, idx, input_type="IP")
        
        # Test Domain input and submit with external links
        if domain:
            print(f"\n{'='*50}")
            print(f"Testing Domain: {domain}")
            print(f"{'='*50}")
            submit_and_test_links(page, search_input, domain, idx, input_type="Domain")
        
        # Test Hash input and submit with external links
        if hash_value:
            print(f"\n{'='*50}")
            print(f"Testing Hash: {hash_value}")
            print(f"{'='*50}")
            submit_and_test_links(page, search_input, hash_value, idx, input_type="Hash")
    
    # Take final screenshot
    page.wait_for_timeout(2000)