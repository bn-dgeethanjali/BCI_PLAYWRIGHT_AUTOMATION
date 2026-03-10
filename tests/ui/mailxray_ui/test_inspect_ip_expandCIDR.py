"""
Test script to test IP address with CIDR notation and expand CIDR functionality.
"""
import sys
import os
import csv
import re

# Add workspace root to path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from pages.locators.login_locators import LoginPageLocators
from utils.config import BASE_URL, USERNAME, PASSWORD


def is_valid_ipv4(ip_string):
    """Check if string is a valid IPv4 address (with or without CIDR notation)."""
    # Pattern for IPv4 with optional CIDR notation
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$'
    
    if not re.match(ipv4_pattern, ip_string):
        return False
    
    # Extract IP part (without CIDR)
    ip_part = ip_string.split('/')[0]
    octets = ip_part.split('.')
    
    # Validate each octet is between 0-255
    for octet in octets:
        if int(octet) > 255:
            return False
    
    return True


def read_ip_testdata_from_csv():
    """Read only IPv4 addresses with CIDR notation from mailxray_homepage.csv file."""
    csv_path = os.path.join(workspace_root, "testdata", "mailxray_homepage.csv")
    ip_addresses = []
    
    with open(csv_path, 'r') as file:
        lines = file.readlines()
        
        # First try to parse as CSV with headers
        file.seek(0)
        try:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Check if 'IP' column exists and has value with CIDR notation
                if 'IP' in row and row['IP']:
                    ip = row['IP'].strip()
                    # Only accept IPs with CIDR notation (containing '/')
                    if '/' in ip and is_valid_ipv4(ip):
                        ip_addresses.append(ip)
                        print(f"Found IPv4 with CIDR from CSV row: {ip}")
        except Exception as e:
            print(f"Note: Could not parse as CSV: {str(e)}")
        
        # Also look for standalone IPv4 addresses with CIDR notation in the file
        for line in lines:
            line = line.strip()
            # Skip header lines or empty lines
            if not line or line.startswith('URL') or line == 'IPV4':
                continue
            
            # Check if line itself is a valid IPv4 address with CIDR notation
            if '/' in line and is_valid_ipv4(line):
                if line not in ip_addresses:
                    ip_addresses.append(line)
                    print(f"Found standalone IPv4 with CIDR: {line}")
    
    return ip_addresses


def test_ip_expand_cidr(page):
    """Test IP address input with CIDR notation and expand CIDR functionality."""
    
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
    
    # Navigate to homepage or IP tools page
    page.goto(BASE_URL + "/")
    
    # Wait for page to fully load
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    
    print(f"Page URL: {page.url}")
    
    # Read IP addresses from CSV
    ip_addresses = read_ip_testdata_from_csv()
    print(f"\nLoaded {len(ip_addresses)} IP addresses from CSV")
    print(f"IP Addresses: {ip_addresses}")
    
    # Try to find IP address input field
    # Try multiple selectors
    ip_input_selectors = [
        'input[placeholder="IP address"]',
        'input[placeholder*="IP address"]',
        'input[placeholder*="IP"]',
        'input[type="text"][placeholder*="IP"]'
    ]
    
    ip_input = None
    for selector in ip_input_selectors:
        try:
            ip_input = page.locator(selector).first
            if ip_input.count() > 0:
                ip_input.wait_for(state="visible", timeout=5000)
                print(f"\n✓ Found IP input field with selector: {selector}")
                break
        except Exception:
            continue
    
    if not ip_input or ip_input.count() == 0:
        print("\n✗ IP input field not found, trying to inspect all inputs...")
        all_inputs = page.locator("input").all()
        for i, inp in enumerate(all_inputs):
            placeholder = inp.get_attribute('placeholder')
            print(f"Input {i}: placeholder='{placeholder}'")
        page.screenshot(path="ip_input_not_found.png", full_page=True)
        return
    
    # Test each IP address
    for idx, ip_address in enumerate(ip_addresses):
        print(f"\n{'='*60}")
        print(f"Testing IP Address {idx + 1}: {ip_address}")
        print(f"{'='*60}")
        
        try:
            # Clear and fill IP input
            ip_input.clear()
            page.wait_for_timeout(500)
            ip_input.fill(ip_address)
            page.wait_for_timeout(1000)
            
            # Verify input
            input_value = ip_input.input_value()
            print(f"✓ IP input successful: {input_value}")
            
            # Take screenshot before submit
            page.screenshot(path=f"ip_input_before_submit_{idx+1}.png")
            print(f"✓ Screenshot saved: ip_input_before_submit_{idx+1}.png")
            
            # Press Enter to submit
            print("\nPressing Enter to submit...")
            ip_input.press('Enter')
            
            # Wait for results to load
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
            print(f"✓ Submit successful. Current URL: {page.url}")
            
            # Take screenshot after submit
            page.screenshot(path=f"ip_results_{idx+1}.png", full_page=True)
            print(f"✓ Screenshot saved: ip_results_{idx+1}.png")
            
            # Look for expand CIDR button/link if CIDR notation is present
            if '/' in ip_address:
                print("\n=== Looking for Expand CIDR functionality ===")
                
                # Try to find expand CIDR button/link
                expand_selectors = [
                    'button:has-text("Expand")',
                    'button:has-text("expand")',
                    'a:has-text("Expand CIDR")',
                    'button:has-text("CIDR")',
                    '[class*="expand"]',
                    'button[class*="expand"]'
                ]
                
                expand_clicked = False
                for selector in expand_selectors:
                    try:
                        expand_btn = page.locator(selector).first
                        if expand_btn.count() > 0:
                            expand_btn.wait_for(state="visible", timeout=3000)
                            print(f"✓ Found expand button with selector: {selector}")
                            expand_btn.click()
                            page.wait_for_timeout(2000)
                            print(f"✓ Clicked expand CIDR button")
                            
                            # Take screenshot after expand
                            page.screenshot(path=f"ip_expanded_cidr_{idx+1}.png", full_page=True)
                            print(f"✓ Screenshot saved: ip_expanded_cidr_{idx+1}.png")
                            expand_clicked = True
                            break
                    except Exception:
                        continue
                
                if not expand_clicked:
                    print("✗ Could not find expand CIDR button")
            
            # Look for common IP-related links (similar to URL test)
            print("\n=== Looking for IP analysis links ===")
            
            # Try to find VirusTotal link
            try:
                virustotal_link = page.locator('a[href*="virustotal"], a:has-text("VirusTotal")').first
                if virustotal_link.count() > 0:
                    virustotal_link.wait_for(state="visible", timeout=3000)
                    print("✓ VirusTotal link found")
                    virustotal_link.click()
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(2000)
                    print(f"✓ VirusTotal clicked. Current URL: {page.url}")
                    page.screenshot(path=f"ip_virustotal_{idx+1}.png", full_page=True)
            except Exception as e:
                print(f"✗ VirusTotal link not found: {str(e)}")
            
        except Exception as e:
            print(f"✗ Error testing IP {ip_address}: {str(e)}")
            page.screenshot(path=f"ip_error_{idx+1}.png", full_page=True)
    
    # Take final screenshot
    page.wait_for_timeout(2000)
    page.screenshot(path="ip_expand_cidr_test_complete.png", full_page=True)
    print("\n✓ All IP tests completed!")
    print("Screenshot saved: ip_expand_cidr_test_complete.png")


def test_inspect_ip_input_fields(page):
    """Inspect page to find IP input fields and expand CIDR elements."""
    
    # Login first
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    page.locator(LoginPageLocators.USERNAME).wait_for(state="visible", timeout=10000)
    
    page.locator(LoginPageLocators.USERNAME).fill(USERNAME)
    page.locator(LoginPageLocators.PASSWORD).fill(PASSWORD)
    page.locator(LoginPageLocators.LOGIN_BUTTON).click()
    
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    
    # Navigate to homepage
    page.goto(BASE_URL + "/")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    
    print(f"\n{'='*60}")
    print("Inspecting page for IP-related elements")
    print(f"{'='*60}")
    
    # Find all input fields
    print("\n=== All Input Fields ===")
    all_inputs = page.locator("input").all()
    for i, inp in enumerate(all_inputs):
        try:
            input_type = inp.get_attribute('type')
            input_placeholder = inp.get_attribute('placeholder')
            input_class = inp.get_attribute('class')
            input_value = inp.get_attribute('value')
            
            print(f"\nInput {i}:")
            print(f"  type: {input_type}")
            print(f"  placeholder: {input_placeholder}")
            print(f"  class: {input_class}")
            print(f"  value: {input_value}")
        except Exception as e:
            print(f"\nInput {i}: Error - {str(e)}")
    
    # Search for elements containing "expand", "CIDR", "IP"
    print("\n=== Searching for CIDR/Expand elements ===")
    keywords = ["expand", "cidr", "ip range"]
    
    for keyword in keywords:
        try:
            elements = page.locator(f"text=/{keyword}/i").all()
            if len(elements) > 0:
                print(f"\n'{keyword}' found in {len(elements)} elements:")
                for i, elem in enumerate(elements[:5]):  # Limit to first 5
                    try:
                        text = elem.text_content()[:100]
                        print(f"  Element {i}: {text}")
                    except:
                        pass
        except Exception as e:
            print(f"Error searching for '{keyword}': {str(e)}")
    
    # Take screenshot
    page.screenshot(path="ip_inspection.png", full_page=True)
    print("\n✓ Inspection complete. Screenshot saved: ip_inspection.png")
