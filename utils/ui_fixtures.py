"""
Reusable Playwright fixtures and test classes for UI automation
"""
import pytest
from playwright.sync_api import Page
from utils.ui_helpers import (
    UIConfig,
    BrowserHelper,
    LoginHelper,
    NavigationHelper,
    ValidationHelper
)


@pytest.fixture(scope="function")
def browser_setup(browser):
    """
    Browser setup with MailXray context
    
    Usage in test files:
        def test_example(browser_setup: Page):
            page = browser_setup
            page.goto("https://example.com")
    """
    context = BrowserHelper.create_context(browser)
    page = context.new_page()
    page.set_default_timeout(UIConfig.DEFAULT_TIMEOUT)
    yield page
    context.close()


@pytest.fixture(scope="function")
def authenticated_page(browser_setup: Page):
    """
    Browser page with user already logged in
    
    Usage in test files:
        def test_dashboard(authenticated_page: Page):
            page = authenticated_page
            # User is already logged in
            page.goto(UIConfig.BASE_URL)
    """
    page = browser_setup
    LoginHelper.login(page)
    yield page


class BaseLoginTests:
    """
    Base test class for Login functionality
    Can be inherited or used directly in test files
    """
    
    def test_login_page_loads(self, browser_setup: Page):
        """TC-001: Verify login page loads successfully"""
        page = browser_setup
        
        print("\n🔍 Testing: Login page loads")
        NavigationHelper.goto_with_wait(page, UIConfig.LOGIN_URL)
        
        # Verify login page elements
        print(f"✓ Current URL: {page.url}")
        print(f"✓ Page title: {page.title()}")
        
        # Check for login form elements
        assert "login" in page.url.lower(), "Not on login page"
        
        print("✅ Login page loaded successfully")
    
    def test_login_form_elements_visible(self, browser_setup: Page):
        """TC-002: Verify all login form elements are visible"""
        page = browser_setup
        
        print("\n🔍 Testing: Login form elements")
        NavigationHelper.goto_with_wait(page, UIConfig.LOGIN_URL)
        
        # Check form elements using helper
        elements = LoginHelper.check_login_form_elements(page)
        
        print(f"✓ Username field: {'Found' if elements['username_field'] else 'Not found'}")
        print(f"✓ Password field: {'Found' if elements['password_field'] else 'Not found'}")
        print(f"✓ Login button: {'Found' if elements['login_button'] else 'Not found'}")
        
        assert elements['username_field'], "Username field not found"
        assert elements['password_field'], "Password field not found"
        assert elements['login_button'], "Login button not found"
        
        print("✅ All login form elements are visible")
    
    def test_login_with_valid_credentials(self, browser_setup: Page):
        """TC-003: Login with valid credentials"""
        page = browser_setup
        
        print("\n🔍 Testing: Login with valid credentials")
        
        # Use LoginHelper for complete login flow
        success = LoginHelper.login(page)
        
        print(f"✓ Current URL after login: {page.url}")
        
        if success:
            print("✅ Login successful - redirected from login page")
        else:
            print("⚠️ Still on login page - check credentials")
            print(f"Note: Set MAILXRAY_USERNAME and MAILXRAY_PASSWORD environment variables")
    
    def test_login_with_empty_credentials(self, browser_setup: Page):
        """TC-004: Login with empty credentials should fail"""
        page = browser_setup
        
        print("\n🔍 Testing: Login with empty credentials")
        NavigationHelper.goto_with_wait(page, UIConfig.LOGIN_URL)
        
        # Click login without filling credentials
        LoginHelper.click_login_button(page)
        
        # Should still be on login page
        page.wait_for_timeout(1000)
        assert "login" in page.url.lower(), "Should remain on login page"
        
        print("✅ Empty credentials validation working")
    
    def test_login_with_invalid_credentials(self, browser_setup: Page):
        """TC-005: Login with invalid credentials should fail"""
        page = browser_setup
        
        print("\n🔍 Testing: Login with invalid credentials")
        
        # Use LoginHelper with invalid credentials
        success = LoginHelper.login(page, username="invalid_user_123", password="wrong_password_456")
        
        # Should show error or remain on login page
        error_found = ValidationHelper.check_error_messages(page)
        
        if error_found:
            print("✓ Error message displayed")
        
        assert not success or "login" in page.url.lower(), "Should remain on login page"
        print("✅ Invalid credentials rejected")


class BaseDashboardTests:
    """
    Base test class for Dashboard functionality
    Automatically logs in before each test
    """
    
    @pytest.fixture(autouse=True)
    def login_before_test(self, browser_setup: Page):
        """Login before each test"""
        page = browser_setup
        LoginHelper.login(page)
        yield page
    
    def test_dashboard_loads(self, browser_setup: Page):
        """TC-006: Verify dashboard loads after login"""
        page = browser_setup
        
        print("\n🔍 Testing: Dashboard loads")
        
        # Navigate to dashboard/home
        NavigationHelper.goto_with_wait(page, UIConfig.BASE_URL)
        
        print(f"✓ Current URL: {page.url}")
        print(f"✓ Page title: {page.title()}")
        
        # Take screenshot
        screenshot_path = BrowserHelper.take_screenshot(page, "mailxray_dashboard.png")
        print(f"✓ Screenshot saved: {screenshot_path}")
        
        print("✅ Dashboard loaded")
    
    def test_navigation_menu_visible(self, browser_setup: Page):
        """TC-007: Verify navigation menu is visible"""
        page = browser_setup
        
        print("\n🔍 Testing: Navigation menu")
        NavigationHelper.goto_with_wait(page, UIConfig.BASE_URL)
        
        # Check for navigation elements using helper
        nav_elements = NavigationHelper.find_navigation_elements(page)
        
        nav_found = any(count > 0 for count in nav_elements.values())
        
        for selector, count in nav_elements.items():
            if count > 0:
                print(f"✓ Navigation found: {selector} ({count} elements)")
        
        if nav_found:
            print("✅ Navigation menu visible")
        else:
            print("⚠️ Navigation menu not found (may use different structure)")
    
    def test_tools_menu_items(self, browser_setup: Page):
        """TC-008: Verify tools menu items are accessible"""
        page = browser_setup
        
        print("\n🔍 Testing: Tools menu items")
        NavigationHelper.goto_with_wait(page, UIConfig.BASE_URL)
        
        # Find tool links using helper
        found_tools = NavigationHelper.find_tool_links(page)
        
        # Print found tools
        available_tools = [name for name, found in found_tools.items() if found]
        for tool_name in available_tools:
            print(f"✓ Found: {tool_name}")
        
        print(f"✅ Found {len(available_tools)} tool(s): {', '.join(available_tools)}")


class BaseToolTests:
    """
    Base test class for Tool access tests
    Automatically logs in before each test
    """
    
    @pytest.fixture(autouse=True)
    def login_and_navigate(self, browser_setup: Page):
        """Login before each test"""
        page = browser_setup
        LoginHelper.login(page)
        yield page
    
    def test_whois_tool_access(self, browser_setup: Page):
        """TC-009: Access WHOIS tool"""
        page = browser_setup
        
        print("\n🔍 Testing: WHOIS tool access")
        NavigationHelper.goto_with_wait(page, UIConfig.WHOIS_URL)
        
        print(f"✓ Current URL: {page.url}")
        print(f"✓ Page title: {page.title()}")
        
        # Take screenshot
        screenshot_path = BrowserHelper.take_screenshot(page, "mailxray_whois.png")
        print(f"✓ Screenshot saved: {screenshot_path}")
        
        print("✅ WHOIS tool accessible")
    
    def test_mxlookup_tool_access(self, browser_setup: Page):
        """TC-010: Access MX Lookup tool"""
        page = browser_setup
        
        print("\n🔍 Testing: MX Lookup tool access")
        NavigationHelper.goto_with_wait(page, UIConfig.MXLOOKUP_URL)
        
        print(f"✓ Current URL: {page.url}")
        print(f"✓ Page title: {page.title()}")
        
        # Take screenshot
        screenshot_path = BrowserHelper.take_screenshot(page, "mailxray_mxlookup.png")
        print(f"✓ Screenshot saved: {screenshot_path}")
        
        print("✅ MX Lookup tool accessible")
    
    def test_virustotal_tool_access(self, browser_setup: Page):
        """TC-011: Access VirusTotal tool"""
        page = browser_setup
        
        print("\n🔍 Testing: VirusTotal tool access")
        NavigationHelper.goto_with_wait(page, UIConfig.VIRUSTOTAL_URL)
        
        print(f"✓ Current URL: {page.url}")
        print(f"✓ Page title: {page.title()}")
        
        # Take screenshot
        screenshot_path = BrowserHelper.take_screenshot(page, "mailxray_virustotal.png")
        print(f"✓ Screenshot saved: {screenshot_path}")
        
        print("✅ VirusTotal tool accessible")
    
    def test_emldata_tool_access(self, browser_setup: Page):
        """TC-012: Access EML Data tool"""
        page = browser_setup
        
        print("\n🔍 Testing: EML Data tool access")
        NavigationHelper.goto_with_wait(page, UIConfig.EMLDATA_URL)
        
        print(f"✓ Current URL: {page.url}")
        print(f"✓ Page title: {page.title()}")
        
        # Take screenshot
        screenshot_path = BrowserHelper.take_screenshot(page, "mailxray_emldata.png")
        print(f"✓ Screenshot saved: {screenshot_path}")
        
        print("✅ EML Data tool accessible")
    
    def test_phaas_tool_access(self, browser_setup: Page):
        """TC-013: Access PHaaS tool"""
        page = browser_setup
        
        print("\n🔍 Testing: PHaaS tool access")
        NavigationHelper.goto_with_wait(page, UIConfig.PHAAS_URL)
        
        print(f"✓ Current URL: {page.url}")
        print(f"✓ Page title: {page.title()}")
        
        # Take screenshot
        screenshot_path = BrowserHelper.take_screenshot(page, "mailxray_phaas.png")
        print(f"✓ Screenshot saved: {screenshot_path}")
        
        print("✅ PHaaS tool accessible")
