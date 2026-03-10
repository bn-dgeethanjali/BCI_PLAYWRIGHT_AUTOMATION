"""
UI Test Helpers and Common Utilities
Provides reusable functions for Playwright UI tests
"""
import os
from playwright.sync_api import Page, Browser
from typing import Optional, Dict, Any


class UIConfig:
    """UI Test Configuration"""
    
    # Application URLs
    BASE_URL = os.getenv("BASE_URL", "https://mailxray.barracudabrts.com")
    LOGIN_URL = f"{BASE_URL}/accounts/login/"
    
    # Test credentials
    TEST_USERNAME = os.getenv("MAILXRAY_USERNAME", "your_username")
    TEST_PASSWORD = os.getenv("MAILXRAY_PASSWORD", "your_password")
    
    # Tool URLs
    WHOIS_URL = f"{BASE_URL}/tools/whois/"
    MXLOOKUP_URL = f"{BASE_URL}/tools/mxlookup/"
    VIRUSTOTAL_URL = f"{BASE_URL}/tools/virustotal/"
    EMLDATA_URL = f"{BASE_URL}/tools/emldata/"
    PHAAS_URL = f"{BASE_URL}/tools/phaas/"
    
    # Browser settings
    DEFAULT_TIMEOUT = 30000
    DEFAULT_VIEWPORT = {"width": 1920, "height": 1080}
    
    # Screenshot settings
    SCREENSHOTS_DIR = "screenshots"


class BrowserHelper:
    """Browser setup and configuration helpers"""
    
    @staticmethod
    def create_context(browser: Browser, **kwargs) -> Any:
        """
        Create a browser context with default configuration
        
        Args:
            browser: Playwright browser instance
            **kwargs: Additional context options
            
        Returns:
            BrowserContext instance
        """
        default_config = {
            "viewport": UIConfig.DEFAULT_VIEWPORT,
            "ignore_https_errors": True
        }
        default_config.update(kwargs)
        return browser.new_context(**default_config)
    
    @staticmethod
    def create_page(browser: Browser, timeout: Optional[int] = None) -> Page:
        """
        Create a page with default configuration
        
        Args:
            browser: Playwright browser instance
            timeout: Custom timeout (default: UIConfig.DEFAULT_TIMEOUT)
            
        Returns:
            Page instance
        """
        context = BrowserHelper.create_context(browser)
        page = context.new_page()
        page.set_default_timeout(timeout or UIConfig.DEFAULT_TIMEOUT)
        return page
    
    @staticmethod
    def take_screenshot(page: Page, filename: str, full_page: bool = True) -> str:
        """
        Take a screenshot and save it
        
        Args:
            page: Playwright page instance
            filename: Screenshot filename
            full_page: Whether to capture full page
            
        Returns:
            Path to saved screenshot
        """
        os.makedirs(UIConfig.SCREENSHOTS_DIR, exist_ok=True)
        screenshot_path = os.path.join(UIConfig.SCREENSHOTS_DIR, filename)
        page.screenshot(path=screenshot_path, full_page=full_page)
        return screenshot_path


class LoginHelper:
    """Login related helper functions"""
    
    # Common selectors for login form elements
    USERNAME_SELECTORS = [
        "input[name='username']",
        "input[name='email']",
        "input[type='text']",
        "#id_username",
        "#username"
    ]
    
    PASSWORD_SELECTORS = [
        "input[name='password']",
        "input[type='password']",
        "#id_password",
        "#password"
    ]
    
    LOGIN_BUTTON_SELECTORS = [
        "button[type='submit']",
        "input[type='submit']",
        "button:has-text('Login')",
        "button:has-text('Sign in')",
        ".btn-login"
    ]
    
    @staticmethod
    def find_element(page: Page, selectors: list) -> Optional[str]:
        """
        Find first matching element from list of selectors
        
        Args:
            page: Playwright page instance
            selectors: List of CSS selectors to try
            
        Returns:
            Matching selector or None
        """
        for selector in selectors:
            if page.locator(selector).count() > 0:
                return selector
        return None
    
    @staticmethod
    def fill_username(page: Page, username: str) -> bool:
        """
        Fill username field
        
        Args:
            page: Playwright page instance
            username: Username to fill
            
        Returns:
            True if successful, False otherwise
        """
        selector = LoginHelper.find_element(page, LoginHelper.USERNAME_SELECTORS)
        if selector:
            page.fill(selector, username)
            return True
        return False
    
    @staticmethod
    def fill_password(page: Page, password: str) -> bool:
        """
        Fill password field
        
        Args:
            page: Playwright page instance
            password: Password to fill
            
        Returns:
            True if successful, False otherwise
        """
        selector = LoginHelper.find_element(page, LoginHelper.PASSWORD_SELECTORS)
        if selector:
            page.fill(selector, password)
            return True
        return False
    
    @staticmethod
    def click_login_button(page: Page) -> bool:
        """
        Click login button
        
        Args:
            page: Playwright page instance
            
        Returns:
            True if successful, False otherwise
        """
        selector = LoginHelper.find_element(page, LoginHelper.LOGIN_BUTTON_SELECTORS)
        if selector:
            page.click(selector)
            return True
        return False
    
    @staticmethod
    def login(
        page: Page,
        username: Optional[str] = None,
        password: Optional[str] = None,
        wait_for_navigation: bool = True
    ) -> bool:
        """
        Complete login flow
        
        Args:
            page: Playwright page instance
            username: Username (defaults to UIConfig.TEST_USERNAME)
            password: Password (defaults to UIConfig.TEST_PASSWORD)
            wait_for_navigation: Whether to wait for page navigation
            
        Returns:
            True if login appears successful, False otherwise
        """
        username = username or UIConfig.TEST_USERNAME
        password = password or UIConfig.TEST_PASSWORD
        
        try:
            # Go to login page
            page.goto(UIConfig.LOGIN_URL)
            page.wait_for_load_state("networkidle")
            
            # Fill credentials
            if not LoginHelper.fill_username(page, username):
                return False
            
            if not LoginHelper.fill_password(page, password):
                return False
            
            # Submit
            if not LoginHelper.click_login_button():
                return False
            
            # Wait for navigation
            if wait_for_navigation:
                page.wait_for_load_state("networkidle", timeout=10000)
            
            # Check if login successful (not on login page anymore)
            return "login" not in page.url.lower()
            
        except Exception as e:
            print(f"⚠️ Login failed: {str(e)}")
            return False
    
    @staticmethod
    def is_logged_in(page: Page) -> bool:
        """
        Check if user is logged in
        
        Args:
            page: Playwright page instance
            
        Returns:
            True if logged in, False otherwise
        """
        # Not on login page indicates logged in
        return "login" not in page.url.lower()
    
    @staticmethod
    def check_login_form_elements(page: Page) -> Dict[str, bool]:
        """
        Check which login form elements are present
        
        Args:
            page: Playwright page instance
            
        Returns:
            Dict with element presence status
        """
        return {
            "username_field": LoginHelper.find_element(page, LoginHelper.USERNAME_SELECTORS) is not None,
            "password_field": LoginHelper.find_element(page, LoginHelper.PASSWORD_SELECTORS) is not None,
            "login_button": LoginHelper.find_element(page, LoginHelper.LOGIN_BUTTON_SELECTORS) is not None
        }


class NavigationHelper:
    """Navigation and page interaction helpers"""
    
    @staticmethod
    def goto_with_wait(page: Page, url: str, wait_state: str = "networkidle") -> None:
        """
        Navigate to URL and wait for load state
        
        Args:
            page: Playwright page instance
            url: URL to navigate to
            wait_state: Load state to wait for
        """
        page.goto(url)
        page.wait_for_load_state(wait_state)
    
    @staticmethod
    def find_navigation_elements(page: Page) -> Dict[str, int]:
        """
        Find navigation elements on page
        
        Args:
            page: Playwright page instance
            
        Returns:
            Dict with element counts
        """
        nav_selectors = ["nav", ".navbar", ".navigation", ".menu", ".sidebar", "header"]
        return {
            selector: page.locator(selector).count()
            for selector in nav_selectors
        }
    
    @staticmethod
    def find_tool_links(page: Page) -> Dict[str, bool]:
        """
        Find MailXray tool links on page
        
        Args:
            page: Playwright page instance
            
        Returns:
            Dict with tool availability status
        """
        tools = {
            "WHOIS": ["a[href*='whois']", "a:has-text('WHOIS')", "a:has-text('Whois')"],
            "MX Lookup": ["a[href*='mxlookup']", "a:has-text('MX Lookup')", "a:has-text('MX')"],
            "VirusTotal": ["a[href*='virustotal']", "a:has-text('VirusTotal')", "a:has-text('VT')"],
            "EML Data": ["a[href*='emldata']", "a:has-text('EML')", "a:has-text('Email')"],
            "PHaaS": ["a[href*='phaas']", "a:has-text('PHaaS')", "a:has-text('Phishing')"],
        }
        
        found_tools = {}
        for tool_name, selectors in tools.items():
            found = False
            for selector in selectors:
                if page.locator(selector).count() > 0:
                    found = True
                    break
            found_tools[tool_name] = found
        
        return found_tools


class ValidationHelper:
    """Validation and assertion helpers"""
    
    @staticmethod
    def check_error_messages(page: Page) -> bool:
        """
        Check if error messages are displayed
        
        Args:
            page: Playwright page instance
            
        Returns:
            True if error found, False otherwise
        """
        error_selectors = [
            ".error",
            ".alert-danger",
            "[role='alert']",
            ".error-message",
            ".invalid-feedback"
        ]
        return any(page.locator(sel).count() > 0 for sel in error_selectors)
    
    @staticmethod
    def is_element_visible(page: Page, selector: str) -> bool:
        """
        Check if element is visible
        
        Args:
            page: Playwright page instance
            selector: CSS selector
            
        Returns:
            True if visible, False otherwise
        """
        try:
            return page.locator(selector).count() > 0 and page.locator(selector).first.is_visible()
        except:
            return False


class ResponsiveHelper:
    """Responsive design testing helpers"""
    
    # Common viewport sizes
    VIEWPORTS = {
        "mobile": {"width": 375, "height": 667},
        "tablet": {"width": 768, "height": 1024},
        "desktop": {"width": 1920, "height": 1080},
        "mobile_landscape": {"width": 667, "height": 375},
        "tablet_landscape": {"width": 1024, "height": 768}
    }
    
    @staticmethod
    def set_viewport(page: Page, device: str) -> None:
        """
        Set viewport to predefined device size
        
        Args:
            page: Playwright page instance
            device: Device name (mobile, tablet, desktop, etc.)
        """
        if device in ResponsiveHelper.VIEWPORTS:
            page.set_viewport_size(ResponsiveHelper.VIEWPORTS[device])
    
    @staticmethod
    def test_responsive_view(page: Page, url: str, device: str, screenshot_name: str) -> str:
        """
        Test responsive view and take screenshot
        
        Args:
            page: Playwright page instance
            url: URL to test
            device: Device name
            screenshot_name: Screenshot filename
            
        Returns:
            Path to screenshot
        """
        ResponsiveHelper.set_viewport(page, device)
        page.goto(url)
        page.wait_for_load_state("networkidle")
        return BrowserHelper.take_screenshot(page, screenshot_name)
