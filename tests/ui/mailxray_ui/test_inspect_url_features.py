"""
Debug script to inspect URL Tools page for URL Protect, Defanged URL, and URL Redirect elements.
"""
import sys
import os

# Add workspace root to path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from pages.locators.login_locators import LoginPageLocators
from utils.config import BASE_URL, USERNAME, PASSWORD


def test_inspect_url_tools_features(page):
    """Inspect URL tools page for URL Protect, Defanged URL, and URL Redirect features."""
    # Login first
    page.goto(BASE_URL)
    page.locator(LoginPageLocators.USERNAME).fill(USERNAME)
    page.locator(LoginPageLocators.PASSWORD).fill(PASSWORD)
    page.locator(LoginPageLocators.LOGIN_BUTTON).click()
    page.wait_for_timeout(2000)
    
    # Navigate to URL tools page and submit a URL
    page.goto(BASE_URL + "/url-tools")
    page.wait_for_timeout(2000)
    
    # Submit a test URL to see results
    page.locator("input[placeholder='Enter URL']").fill("https://google.com")
    page.locator("input[placeholder='Enter URL']").press("Enter")
    page.wait_for_timeout(3000)
    
    print(f"\nURL Tools Page URL: {page.url}")
    
    # Search for elements containing "protect", "defang", "redirect"
    print("\n=== Searching for URL Protect elements ===")
    protect_elements = page.locator("text=/protect/i").all()
    for i, elem in enumerate(protect_elements):
        print(f"Protect {i}: {elem.text_content()[:100]}")
    
    print("\n=== Searching for Defanged URL elements ===")
    defang_elements = page.locator("text=/defang/i").all()
    for i, elem in enumerate(defang_elements):
        print(f"Defang {i}: {elem.text_content()[:100]}")
    
    print("\n=== Searching for URL Redirect elements ===")
    redirect_elements = page.locator("text=/redirect/i").all()
    for i, elem in enumerate(redirect_elements):
        print(f"Redirect {i}: {elem.text_content()[:100]}")
    
    # Find all buttons
    print("\n=== All Buttons ===")
    all_buttons = page.locator("button").all()
    for i, btn in enumerate(all_buttons):
        btn_text = btn.text_content()
        if btn_text and len(btn_text.strip()) > 0:
            print(f"Button {i}: {btn_text[:100]}")
    
    # Find all divs with text
    print("\n=== Looking for result sections ===")
    result_divs = page.locator("div").all()
    for i, div in enumerate(result_divs[:50]):  # Limit to first 50
        div_text = div.text_content()
        if div_text and any(keyword in div_text.lower() for keyword in ['protect', 'defang', 'redirect']):
            print(f"\nDiv {i}: {div_text[:150]}")
            print(f"  Class: {div.get_attribute('class')}")
    
    # Click on tabs/buttons for 'protect', 'defang', 'redirect'
    keywords = ['protect', 'defang', 'redirect']
    
    for keyword in keywords:
        print(f"\n{'='*60}")
        print(f"Testing '{keyword}' feature")
        print(f"{'='*60}")
        
        try:
            # Try to find and click button/tab containing the keyword
            # Try multiple selectors: button, div with role=button, clickable elements
            clickable_selectors = [
                f"button:has-text('{keyword}')",
                f"div:has-text('{keyword}')[role='button']",
                f"[role='tab']:has-text('{keyword}')",
                f"a:has-text('{keyword}')",
                f"div[class*='tab']:has-text('{keyword}')",
                f"div[class*='button']:has-text('{keyword}')"
            ]
            
            clicked = False
            for selector in clickable_selectors:
                try:
                    element = page.locator(selector).first
                    if element.count() > 0:
                        element.wait_for(state="visible", timeout=3000)
                        print(f"✓ Found '{keyword}' element with selector: {selector}")
                        element.click()
                        page.wait_for_timeout(2000)
                        print(f"✓ Clicked on '{keyword}' tab/button")
                        
                        # Take screenshot
                        clicked = True
                        break
                except Exception:
                    continue
            
            if not clicked:
                print(f"✗ Could not find clickable element for '{keyword}'")
                
        except Exception as e:
            print(f"✗ Error clicking '{keyword}': {str(e)}")
    
    # Take screenshot
