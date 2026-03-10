"""
Test script to test Email Viewer functionality - upload and view .eml files.
"""
import sys
import os
import glob

# Add workspace root to path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from pages.locators.login_locators import LoginPageLocators
from utils.config import BASE_URL, USERNAME, PASSWORD


def read_eml_files_from_csv():
    """Read .eml file paths from mailxray_homepage.csv and find .eml files in testdata."""
    csv_path = os.path.join(workspace_root, "testdata", "mailxray_homepage.csv")
    eml_files = []
    
    with open(csv_path, 'r') as file:
        lines = file.readlines()
        
        # Look for "Email files" section
        found_email_section = False
        for i, line in enumerate(lines):
            line = line.strip()
            
            if 'Email files' in line or 'Email Files' in line or 'EML Files' in line:
                found_email_section = True
                print(f"Found Email files section in CSV at line {i+1}")
                continue
            
            # Get file path after the Email files label
            if found_email_section and line:
                # Stop if we hit another section
                if line.startswith(('URL', 'IP', 'Domain', 'Hash', 'IPV4', 'Base64', 'QR')):
                    break
                
                # Check if it's a directory path
                if '/' in line or '\\' in line:
                    print(f"Found email path from CSV: {line}")
                    
                    # Expand user path (~)
                    expanded_path = os.path.expanduser(line)
                    
                    if os.path.exists(expanded_path):
                        # If it's a directory, find .eml files in it
                        if os.path.isdir(expanded_path):
                            eml_pattern = os.path.join(expanded_path, "*.eml")
                            found_files = glob.glob(eml_pattern)
                            eml_files.extend(found_files)
                            print(f"✓ Found {len(found_files)} .eml file(s) in: {expanded_path}")
                        # If it's a file
                        elif line.endswith('.eml'):
                            eml_files.append(expanded_path)
                            print(f"✓ Found .eml file: {expanded_path}")
                    else:
                        print(f"✗ Path not found: {expanded_path}")
                    
                    found_email_section = False
    
    # Also check testdata folder for .eml files
    testdata_path = os.path.join(workspace_root, "testdata")
    if os.path.exists(testdata_path):
        testdata_eml_files = glob.glob(os.path.join(testdata_path, "*.eml"))
        for eml_file in testdata_eml_files:
            if eml_file not in eml_files:
                eml_files.append(eml_file)
                print(f"✓ Found .eml file in testdata: {os.path.basename(eml_file)}")
    
    return eml_files


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


def test_email_viewer(page):
    """Test Email Viewer functionality - upload and view .eml files."""
    
    # Login
    login_to_application(page)
    
    # Navigate to homepage
    page.goto(BASE_URL + "/")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    print(f"✓ Navigated to homepage: {page.url}")
    
    # Read .eml files
    eml_files = read_eml_files_from_csv()
    
    if not eml_files:
        print("\n✗ No .eml files found")
        page.screenshot(path="email_viewer_no_files.png")
        return
    
    print(f"\n✓ Loaded {len(eml_files)} .eml file(s)")
    
    # Click Email Viewer button (SVG icon)
    print("\n=== Clicking Email Viewer button ===")
    
    email_viewer_selectors = [
        'svg:has(> path[d*="15.6458"])',  # Unique path from the SVG
        '*:has(> svg.hover\\:cursor-pointer)',
        'svg[width="24"][height="22"]',
        'button:has-text("Email")',
        'a:has-text("Email")',
        'text=/email.*viewer|viewer.*email/i'
    ]
    
    email_button = find_element_by_selectors(page, email_viewer_selectors, "Email Viewer button")
    
    if email_button:
        email_button.click()
        page.wait_for_timeout(1500)
        print("✓ Clicked Email Viewer button")
        page.screenshot(path="email_viewer_opened.png")
    else:
        print("✗ Email Viewer button not found, trying inspection...")
        inspect_email_viewer_elements(page)
        return
    
    # Upload and view .eml files
    for idx, eml_file in enumerate(eml_files):
        print(f"\n{'='*60}")
        print(f"Processing Email File {idx + 1}: {os.path.basename(eml_file)}")
        print(f"{'='*60}")
        
        try:
            # Look for file input
            file_input = page.locator('input[type="file"]').first
            
            if file_input.count() > 0:
                print(f"✓ Found file input, uploading: {eml_file}")
                file_input.set_input_files(eml_file)
                
                # Wait for processing
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(3000)
                print(f"✓ Email file uploaded and processed")
                
                # Capture viewer
                page.screenshot(path=f"email_viewer_{idx+1}.png", full_page=True)
                
                # Try to extract email content/headers
                content_selectors = [
                    'div[class*="email"]',
                    'div[class*="content"]',
                    'div[class*="message"]',
                    'pre',
                    'iframe',
                    'div[class*="viewer"]'
                ]
                
                for selector in content_selectors:
                    try:
                        content = page.locator(selector).first
                        if content.count() > 0:
                            # For iframe, switch context
                            if selector == 'iframe':
                                frame = content
                                frame_content = frame.content_frame()
                                if frame_content:
                                    text = frame_content.locator('body').text_content()
                                    if text:
                                        print(f"✓ Email content (iframe): {text[:150]}...")
                                        break
                            else:
                                text = content.text_content() or ""
                                if text.strip():
                                    print(f"✓ Email content: {text[:150]}...")
                                    break
                    except:
                        continue
                
                # Look for email headers (From, To, Subject)
                print("\n=== Email headers ===")
                header_keywords = ['from:', 'to:', 'subject:', 'date:']
                for keyword in header_keywords:
                    try:
                        header_elem = page.locator(f'text=/{keyword}/i').first
                        if header_elem.count() > 0:
                            header_text = header_elem.text_content()
                            print(f"  {header_text[:100]}")
                    except:
                        pass
                
            else:
                print("✗ File input not found")
                page.screenshot(path=f"email_no_input_{idx+1}.png")
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            page.screenshot(path=f"email_error_{idx+1}.png")
    
    # Final screenshot
    page.screenshot(path="email_viewer_test_complete.png", full_page=True)
    print("\n✓ Email viewer test completed!")


def inspect_email_viewer_elements(page):
    """Helper function to inspect Email Viewer elements."""
    print(f"\n{'='*60}")
    print("Email Viewer Element Inspection")
    print(f"{'='*60}\n")
    
    # Find SVGs
    print("=== SVG Elements ===")
    svgs = page.locator("svg").all()
    print(f"Found {len(svgs)} SVG element(s)")
    for i, svg in enumerate(svgs[:10]):
        try:
            width = svg.get_attribute('width')
            height = svg.get_attribute('height')
            if width and height:
                print(f"  SVG {i}: {width}x{height}")
        except:
            pass
    
    # Find file inputs
    print("\n=== File Inputs ===")
    file_inputs = page.locator('input[type="file"]').all()
    print(f"Found {len(file_inputs)} file input(s)")
    for i, inp in enumerate(file_inputs):
        accept = inp.get_attribute('accept') or 'any'
        print(f"  Input {i}: accept={accept}")
    
    # Search for email-related elements
    print("\n=== Email-Related Elements ===")
    for keyword in ["email", "eml", "viewer", "browse", "upload"]:
        elements = page.locator(f"text=/{keyword}/i").all()
        if elements:
            print(f"'{keyword}': {len(elements)} element(s)")
    
    #page.screenshot(path="email_viewer_inspection.png", full_page=True)
    #print("\n✓ Inspection screenshot saved: email_viewer_inspection.png")


def test_inspect_email_viewer_page(page):
    """Standalone inspection test for Email Viewer elements."""
    login_to_application(page)
    page.goto(BASE_URL + "/")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)
    inspect_email_viewer_elements(page)
