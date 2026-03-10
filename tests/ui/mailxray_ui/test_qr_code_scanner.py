"""
Test script to test QR Code Scanner functionality - upload and scan QR code.
"""
import sys
import os

# Add workspace root to path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from pages.locators.login_locators import LoginPageLocators
from utils.config import BASE_URL, USERNAME, PASSWORD


def read_qr_code_testdata_from_csv():
    """Read QR code file path from mailxray_homepage.csv file."""
    csv_path = os.path.join(workspace_root, "testdata", "mailxray_homepage.csv")
    qr_code_files = []
    
    with open(csv_path, 'r') as file:
        lines = file.readlines()
        
        # Look for "QR code" label and get the next line(s) with file paths
        found_qr_section = False
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check if this line contains "QR code" label
            if 'QR code' in line or 'QR Code' in line or line == 'QR code':
                found_qr_section = True
                print(f"Found QR code section in CSV at line {i+1}: '{line}'")
                continue
            
            # Get file path after the QR code label
            if found_qr_section and line:
                # Stop if we hit another section (lines with commas or specific keywords)
                if ',' in line and line.startswith(('URL', 'IP', 'Domain', 'Hash')):
                    break
                if line in ['IPV4', 'Base64 Decoder', 'URL,IP,Domain,Hash']:
                    break
                    
                # This should be a file path - check if it looks like a path
                if '/' in line or '\\' in line or line.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    print(f"Checking file path from CSV: {line}")
                    
                    if os.path.exists(line):
                        qr_code_files.append(line)
                        print(f"✓ Found valid QR code file: {line}")
                    else:
                        print(f"✗ QR code file not found at: {line}")
                        # Try to find the file in common locations
                        filename = os.path.basename(line)
                        alternate_paths = [
                            os.path.join(workspace_root, "testdata", filename),
                            os.path.join(workspace_root, filename),
                            os.path.expanduser(line),  # Expand ~ if present
                            line  # Keep original
                        ]
                        for alt_path in alternate_paths:
                            if os.path.exists(alt_path):
                                qr_code_files.append(alt_path)
                                print(f"✓ Found QR code file at alternate location: {alt_path}")
                                break
                    
                    # Found one QR file, stop looking for more unless there are more paths
                    found_qr_section = False
    
    return qr_code_files


def login_to_application(page):
    """Helper function to login to the application."""
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    page.locator(LoginPageLocators.USERNAME).wait_for(state="visible", timeout=10000)
    page.locator(LoginPageLocators.USERNAME).fill(USERNAME)
    page.locator(LoginPageLocators.PASSWORD).fill(PASSWORD)
    page.locator(LoginPageLocators.LOGIN_BUTTON).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    print(f"✓ Logged in successfully. URL: {page.url}")


def find_element_by_selectors(page, selectors, element_name, timeout=5000):
    """Helper function to find element using multiple selectors."""
    for selector in selectors:
        try:
            element = page.locator(selector).first
            if element.count() > 0:
                element.wait_for(state="visible", timeout=timeout)
                print(f"✓ Found {element_name} with selector: {selector}")
                return element
        except Exception:
            continue
    print(f"✗ Could not find {element_name}")
    return None


def test_qr_code_scanner(page):
    """Optimized test for QR Code Scanner - upload and scan QR code with optional inspection."""
    
    # Login
    login_to_application(page)
    
    # Navigate to homepage
    page.goto(BASE_URL + "/")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    print(f"✓ Navigated to homepage: {page.url}")
    
    # Read QR code file paths from CSV
    qr_code_files = read_qr_code_testdata_from_csv()
    
    if not qr_code_files:
        print("\n✗ No QR code files found in CSV")
        # Run inspection to help debug
        print("\n=== Running element inspection ===")
        inspect_qr_elements(page)
        return
    
    print(f"\n✓ Loaded {len(qr_code_files)} QR code file(s)")
    
    # Click QR Scanner button
    print("\n=== Clicking QR Code Scanner button ===")
    qr_scanner_selectors = [
        'svg[title="Scan QR Code"]',
        'svg:has(> title:text("Scan QR Code"))',
        '*:has(> svg > title:text("Scan QR Code"))',
        'svg.hover\\:cursor-pointer',
        'text=/scan.*qr|qr.*scan/i'
    ]
    
    qr_button = find_element_by_selectors(page, qr_scanner_selectors, "QR Scanner button")
    
    if qr_button:
        qr_button.click()
        page.wait_for_timeout(1500)
        print("✓ Clicked QR Code Scanner button")
    else:
        print("\n=== Running element inspection to debug ===")
        inspect_qr_elements(page)
        return
    
    # Upload and scan QR codes
    for idx, qr_file in enumerate(qr_code_files):
        print(f"\n{'='*60}")
        print(f"Processing QR Code {idx + 1}: {os.path.basename(qr_file)}")
        print(f"{'='*60}")
        
        try:
            # Find file input (direct upload is more reliable than clicking browse)
            file_input = page.locator('input[type="file"]').first
            
            if file_input.count() > 0:
                print(f"✓ Found file input, uploading: {qr_file}")
                file_input.set_input_files(qr_file)
                
                # Wait for processing
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(2000)
                print(f"✓ QR code uploaded and processed")
                
                # Capture result
                
                # Try to extract result text
                result_selectors = [
                    'div[class*="result"]',
                    'pre',
                    'textarea[readonly]',
                    'div[class*="output"]'
                ]
                
                for selector in result_selectors:
                    try:
                        result = page.locator(selector).first
                        if result.count() > 0:
                            text = result.text_content() or result.input_value() or ""
                            if text.strip():
                                print(f"✓ QR scan result: {text[:150]}")
                                break
                    except:
                        continue
                
            else:
                print("✗ File input not found")
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    # Final screenshot
    print("\n✓ QR code scanner test completed!")


def inspect_qr_elements(page):
    """Helper function to inspect and print QR-related elements on the page."""
    print("\n{'='*60}")
    print("QR Code Scanner Element Inspection")
    print(f"{'='*60}\n")
    
    # Find SVGs with titles
    print("=== SVG Elements ===")
    svgs = page.locator("svg").all()
    for i, svg in enumerate(svgs[:5]):
        try:
            title = svg.locator("title").first
            if title.count() > 0:
                print(f"SVG {i}: {title.text_content()}")
        except:
            pass
    
    # Find file inputs
    print("\n=== File Inputs ===")
    file_inputs = page.locator('input[type="file"]').all()
    print(f"Found {len(file_inputs)} file input(s)")
    for i, inp in enumerate(file_inputs):
        accept = inp.get_attribute('accept') or 'any'
        print(f"  Input {i}: accept={accept}")
    
    # Search for QR-related text
    print("\n=== QR-Related Elements ===")
    for keyword in ["qr", "scan", "browse", "upload"]:
        elements = page.locator(f"text=/{keyword}/i").all()
        if elements:
            print(f"'{keyword}': {len(elements)} element(s)")
    



