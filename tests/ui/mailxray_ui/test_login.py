import sys
import os

# Add workspace root to path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from playwright.sync_api import expect
from pages.locators.login_locators import LoginPageLocators
from utils.config import BASE_URL, USERNAME, PASSWORD

def test_login(page):
    page.goto(BASE_URL)
    print(f"Navigated to: {page.url}")
    
    # Wait for page to load
    page.wait_for_load_state("networkidle")
    
    # Check if username field exists
    username_field = page.locator(LoginPageLocators.USERNAME)
    print(f"Username locator: {LoginPageLocators.USERNAME}")
    print(f"Username field count: {username_field.count()}")
    
    # Check if password field exists
    password_field = page.locator(LoginPageLocators.PASSWORD)
    print(f"Password locator: {LoginPageLocators.PASSWORD}")
    print(f"Password field count: {password_field.count()}")
    
    # Check if button exists
    button = page.locator(LoginPageLocators.LOGIN_BUTTON)
    print(f"Login button locator: {LoginPageLocators.LOGIN_BUTTON}")
    print(f"Login button count: {button.count()}")
    
    # If locators don't find elements, print all input fields
    if username_field.count() == 0:
        print("\n=== All input fields on page ===")
        all_inputs = page.locator("input").all()
        for i, inp in enumerate(all_inputs):
            print(f"Input {i}: type={inp.get_attribute('type')}, name={inp.get_attribute('name')}, id={inp.get_attribute('id')}, placeholder={inp.get_attribute('placeholder')}")
        
        print("\n=== All buttons on page ===")
        all_buttons = page.locator("button").all()
        for i, btn in enumerate(all_buttons):
            print(f"Button {i}: text={btn.text_content()}, type={btn.get_attribute('type')}, id={btn.get_attribute('id')}")
    
    # Try to fill fields
    username_field.fill(USERNAME)
    print(f"Filled username: {USERNAME}")
    
    password_field.fill(PASSWORD)
    print("Filled password")
    
    # Take screenshot before clicking
    
    button.click()
    print("Clicked login button")
    
    # Wait a moment for any response
    page.wait_for_timeout(3000)
    print(f"Current URL after click: {page.url}")
    
    # Take screenshot after clicking
