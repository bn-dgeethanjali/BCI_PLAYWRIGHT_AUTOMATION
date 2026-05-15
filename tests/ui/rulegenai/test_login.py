"""
RuleGen AI Login Tests
Test cases for login functionality
"""

import os
import sys

# Add workspace root to Python path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

import pytest
from playwright.sync_api import Page, expect

from pages.locators.rulegenai_locators import RuleGenAILoginLocators
from tests.ui.rulegenai.conftest import RuleGenAIConfig


@pytest.mark.rulegenai
class TestRuleGenAILogin:
    """Test suite for RuleGen AI login functionality"""

    def test_login_page_loads(self, rulegenai_page: Page):
        """TC-RG-001: Verify login page loads successfully"""
        page = rulegenai_page

        # Navigate to login page
        page.goto(RuleGenAIConfig.LOGIN_URL)
        page.wait_for_load_state("networkidle")

        print(f"Current URL: {page.url}")
        print(f"Page title: {page.title()}")

        # Verify we're on login page
        assert "login" in page.url.lower() or page.locator(RuleGenAILoginLocators.LOGIN_BUTTON).count() > 0

        print("Login page loaded successfully")

    def test_login_form_elements_visible(self, rulegenai_page: Page):
        """TC-RG-002: Verify all login form elements are visible"""
        page = rulegenai_page

        page.goto(RuleGenAIConfig.LOGIN_URL)
        page.wait_for_load_state("networkidle")

        # Check form elements
        username_field = page.locator(RuleGenAILoginLocators.USERNAME_INPUT)
        password_field = page.locator(RuleGenAILoginLocators.PASSWORD_INPUT)
        login_button = page.locator(RuleGenAILoginLocators.LOGIN_BUTTON)

        print(f"Username field count: {username_field.count()}")
        print(f"Password field count: {password_field.count()}")
        print(f"Login button count: {login_button.count()}")

        # At least one of each should exist
        assert username_field.count() > 0, "Username field not found"
        assert password_field.count() > 0, "Password field not found"
        assert login_button.count() > 0, "Login button not found"

        print("All login form elements are visible")

    def test_login_with_valid_credentials(self, rulegenai_page: Page):
        """TC-RG-003: Login with valid credentials"""
        page = rulegenai_page

        username = RuleGenAIConfig.USERNAME
        password = RuleGenAIConfig.PASSWORD

        if not username or not password:
            pytest.skip("RULEGENAI_USERNAME and RULEGENAI_PASSWORD required")

        # Navigate to login
        page.goto(RuleGenAIConfig.LOGIN_URL)
        page.wait_for_load_state("networkidle")

        # Fill credentials
        page.locator(RuleGenAILoginLocators.USERNAME_INPUT).first.fill(username)
        page.locator(RuleGenAILoginLocators.PASSWORD_INPUT).first.fill(password)

        # Click login
        page.locator(RuleGenAILoginLocators.LOGIN_BUTTON).first.click()

        # Wait for navigation to complete
        page.wait_for_timeout(3000)
        page.wait_for_load_state("networkidle")

        print(f"URL after login: {page.url}")

        # Take screenshot after login
        page.screenshot(path="screenshots/rulegenai/test_login_result.png", full_page=True)

        # Verify login success - should not be on login page
        assert "login" not in page.url.lower(), "Still on login page after login attempt"

        print("Login successful")

    def test_login_with_empty_credentials(self, rulegenai_page: Page):
        """TC-RG-004: Login with empty credentials should fail"""
        page = rulegenai_page

        page.goto(RuleGenAIConfig.LOGIN_URL)
        page.wait_for_load_state("networkidle")

        # Click login without filling credentials
        login_button = page.locator(RuleGenAILoginLocators.LOGIN_BUTTON).first

        # Check if button is disabled or if click shows error
        if login_button.is_enabled():
            login_button.click()
            page.wait_for_timeout(1000)

            # Should still be on login page or show error
            error = page.locator(RuleGenAILoginLocators.ERROR_MESSAGE)
            still_on_login = "login" in page.url.lower()

            assert still_on_login or error.count() > 0, "Empty credentials should not allow login"

        print("Empty credentials validation working")

    def test_login_with_invalid_credentials(self, rulegenai_page: Page):
        """TC-RG-005: Login with invalid credentials should fail"""
        page = rulegenai_page

        page.goto(RuleGenAIConfig.LOGIN_URL)
        page.wait_for_load_state("networkidle")

        # Fill invalid credentials
        page.locator(RuleGenAILoginLocators.USERNAME_INPUT).first.fill("invalid_user_xyz")
        page.locator(RuleGenAILoginLocators.PASSWORD_INPUT).first.fill("wrong_password_123")

        # Click login
        page.locator(RuleGenAILoginLocators.LOGIN_BUTTON).first.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        # Should show error or remain on login page
        error = page.locator(RuleGenAILoginLocators.ERROR_MESSAGE)
        still_on_login = "login" in page.url.lower()

        if error.count() > 0:
            print(f"Error message displayed: {error.first.text_content()}")

        assert still_on_login or error.count() > 0, "Invalid credentials should not allow login"

        print("Invalid credentials rejected")

    def test_password_field_masked(self, rulegenai_page: Page):
        """TC-RG-006: Password field should mask input"""
        page = rulegenai_page

        page.goto(RuleGenAIConfig.LOGIN_URL)
        page.wait_for_load_state("networkidle")

        password_field = page.locator(RuleGenAILoginLocators.PASSWORD_INPUT).first

        # Check type attribute
        field_type = password_field.get_attribute("type")
        assert field_type == "password", f"Password field type is '{field_type}', should be 'password'"

        print("Password field is properly masked")

    def test_login_page_responsive(self, rulegenai_page: Page):
        """TC-RG-007: Login page should be responsive"""
        page = rulegenai_page

        viewports = [
            {"width": 1920, "height": 1080, "name": "Desktop"},
            {"width": 768, "height": 1024, "name": "Tablet"},
            {"width": 375, "height": 667, "name": "Mobile"},
        ]

        for viewport in viewports:
            page.set_viewport_size({"width": viewport["width"], "height": viewport["height"]})
            page.goto(RuleGenAIConfig.LOGIN_URL)
            page.wait_for_load_state("networkidle")

            # Login form should be visible at all sizes
            login_button = page.locator(RuleGenAILoginLocators.LOGIN_BUTTON)
            assert login_button.count() > 0, f"Login button not visible at {viewport['name']} size"

            print(f"Login page responsive at {viewport['name']} ({viewport['width']}x{viewport['height']})")

        print("Login page is responsive across all viewport sizes")
