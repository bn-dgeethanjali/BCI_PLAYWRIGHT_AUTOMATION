"""
Test script to test Base64 Decoder functionality.
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


def read_base64_testdata_from_csv():
    """Read Base64 Decoder test data from mailxray_homepage.csv file."""
    csv_path = os.path.join(workspace_root, "testdata", "mailxray_homepage.csv")
    base64_data = []
    
    with open(csv_path, 'r') as file:
        lines = file.readlines()
        
        # Look for "Base64 Decoder" label and get the next line
        found_base64_section = False
        for line in lines:
            line = line.strip()
            
            if line == 'Base64 Decoder':
                found_base64_section = True
                print("Found Base64 Decoder section in CSV")
                continue
            
            # Get data after the Base64 Decoder label
            if found_base64_section and line:
                # Stop if we hit another section
                if any(keyword in line for keyword in ['URL,', 'IPV4', 'Domain']):
                    break
                base64_data.append(line)
                print(f"Found Base64 data: {line}")
    
    return base64_data


def test_base64_decoder(page):
    """Test Base64 Decoder functionality with data from CSV."""
    
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
    
    # Wait for page to fully load
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    
    print(f"Page URL: {page.url}")
    
    # Read Base64 test data from CSV
    base64_data = read_base64_testdata_from_csv()
    
    if not base64_data:
        print("\n✗ No Base64 test data found in CSV")
        return
    
    print(f"\nLoaded {len(base64_data)} Base64 entries from CSV")
    
    # Click on Base64 Decoder tab/link
    print("\n=== Looking for Base64 Decoder tab ===")
    
    # Try multiple selectors to find the Base64 Decoder tab/link
    base64_selectors = [
        'a:has-text("Base64 Decoder")',
        'button:has-text("Base64 Decoder")',
        'a:has-text("Base64")',
        'button:has-text("Base64")',
        '[href*="base64"]',
        'div:has-text("Base64 Decoder")[role="button"]',
        'div[class*="tab"]:has-text("Base64")'
    ]
    
    tab_clicked = False
    for selector in base64_selectors:
        try:
            base64_tab = page.locator(selector).first
            if base64_tab.count() > 0:
                base64_tab.wait_for(state="visible", timeout=5000)
                print(f"✓ Found Base64 Decoder tab with selector: {selector}")
                base64_tab.click()
                page.wait_for_timeout(2000)
                print(f"✓ Clicked Base64 Decoder tab")
                tab_clicked = True
                break
        except Exception as e:
            continue
    
    if not tab_clicked:
        print("✗ Could not find Base64 Decoder tab, trying to navigate directly...")
        try:
            page.goto(BASE_URL + "/base64-decoder")
            page.wait_for_timeout(2000)
            print("✓ Navigated to Base64 Decoder page directly")
        except Exception as e:
            print(f"✗ Could not navigate to Base64 Decoder: {str(e)}")
            return
    
    # Find the textarea for Base64 input
    print("\n=== Looking for Base64 input textarea ===")
    
    textarea_selectors = [
        'textarea[placeholder="Enter encoded text..."]',
        'textarea[placeholder*="encoded"]',
        'textarea[placeholder*="text"]',
        'textarea'
    ]
    
    base64_textarea = None
    for selector in textarea_selectors:
        try:
            base64_textarea = page.locator(selector).first
            if base64_textarea.count() > 0:
                base64_textarea.wait_for(state="visible", timeout=5000)
                print(f"✓ Found Base64 textarea with selector: {selector}")
                break
        except Exception:
            continue
    
    if not base64_textarea or base64_textarea.count() == 0:
        print("\n✗ Base64 textarea not found")
        return
    
    # Test each Base64 entry
    for idx, base64_text in enumerate(base64_data):
        print(f"\n{'='*60}")
        print(f"Testing Base64 Entry {idx + 1}: {base64_text}")
        print(f"{'='*60}")
        
        try:
            # Clear and fill textarea
            base64_textarea.clear()
            page.wait_for_timeout(500)
            base64_textarea.fill(base64_text)
            page.wait_for_timeout(1000)
            
            # Verify input
            input_value = base64_textarea.input_value()
            print(f"✓ Base64 input successful: {input_value}")
            
            # Take screenshot after input
            
            # Look for decode button
            print("\n=== Looking for Decode button ===")
            
            decode_button_selectors = [
                'button:has-text("Decode")',
                'button:has-text("decode")',
                'button[type="submit"]',
                'button:has-text("Submit")'
            ]
            
            decode_clicked = False
            for selector in decode_button_selectors:
                try:
                    decode_btn = page.locator(selector).first
                    if decode_btn.count() > 0:
                        decode_btn.wait_for(state="visible", timeout=3000)
                        print(f"✓ Found Decode button with selector: {selector}")
                        decode_btn.click()
                        page.wait_for_timeout(2000)
                        print(f"✓ Clicked Decode button")
                        
                        # Take screenshot after decode
                        decode_clicked = True
                        break
                except Exception:
                    continue
            
            if not decode_clicked:
                print("✗ Could not find Decode button")
            
            # Look for decoded output
            print("\n=== Looking for decoded output ===")
            
            # Try to find output textarea or div
            output_selectors = [
                'textarea[placeholder*="Decoded"]',
                'textarea[placeholder*="decoded"]',
                'div[class*="output"]',
                'div[class*="result"]',
                'pre'
            ]
            
            for selector in output_selectors:
                try:
                    output_elem = page.locator(selector).first
                    if output_elem.count() > 0:
                        output_elem.wait_for(state="visible", timeout=3000)
                        output_text = output_elem.text_content() or output_elem.input_value()
                        if output_text:
                            print(f"✓ Found decoded output: {output_text[:100]}")
                            break
                except Exception:
                    continue
            
        except Exception as e:
            print(f"✗ Error testing Base64 entry: {str(e)}")
    
    # Take final screenshot
    page.wait_for_timeout(2000)


def test_inspect_base64_decoder_page(page):
    """Inspect Base64 Decoder page to find correct selectors."""
    
    # Login first
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    page.locator(LoginPageLocators.USERNAME).wait_for(state="visible", timeout=10000)
    
    page.locator(LoginPageLocators.USERNAME).fill(USERNAME)
    page.locator(LoginPageLocators.PASSWORD).fill(PASSWORD)
    page.locator(LoginPageLocators.LOGIN_BUTTON).click()
    
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    
    # Try to navigate to base64 decoder
    page.goto(BASE_URL + "/")
    page.wait_for_timeout(2000)
    
    print(f"\n{'='*60}")
    print("Inspecting page for Base64 Decoder elements")
    print(f"{'='*60}")
    
    # Find all textareas
    print("\n=== All Textarea Fields ===")
    all_textareas = page.locator("textarea").all()
    for i, textarea in enumerate(all_textareas):
        try:
            textarea_placeholder = textarea.get_attribute('placeholder')
            textarea_class = textarea.get_attribute('class')
            
            print(f"\nTextarea {i}:")
            print(f"  placeholder: {textarea_placeholder}")
            print(f"  class: {textarea_class}")
        except Exception as e:
            print(f"\nTextarea {i}: Error - {str(e)}")
    
    # Search for Base64 related elements
    print("\n=== Searching for Base64 elements ===")
    try:
        base64_elements = page.locator("text=/base64/i").all()
        if len(base64_elements) > 0:
            print(f"\nFound {len(base64_elements)} elements containing 'base64':")
            for i, elem in enumerate(base64_elements[:10]):
                try:
                    text = elem.text_content()[:100]
                    print(f"  Element {i}: {text}")
                except:
                    pass
    except Exception as e:
        print(f"Error searching for Base64 elements: {str(e)}")
    
    # Take screenshot
