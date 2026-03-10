import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import os
import sys
from datetime import datetime

# Add workspace root to Python path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from resources.playwright_config import PlaywrightConfig


@pytest.fixture(scope="session")
def browser():
    """Session-scoped browser instance"""
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, PlaywrightConfig.BROWSER)
        browser = browser_type.launch(**PlaywrightConfig.get_browser_config())
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Function-scoped browser context"""
    PlaywrightConfig.ensure_directories()
    context = browser.new_context(**PlaywrightConfig.get_context_config())
    context.set_default_timeout(PlaywrightConfig.TIMEOUT)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, request):
    """Function-scoped page instance with screenshot on failure"""
    page = context.new_page()
    
    yield page
    
    
    page.close()


@pytest.fixture(scope="function")
def authenticated_page(page: Page):
    """Function-scoped authenticated page (with login)"""
    from utils.login_page import LoginPage
    
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(
        username=PlaywrightConfig.TEST_USERNAME,
        password=PlaywrightConfig.TEST_PASSWORD
    )
    
    # Verify login was successful
    assert login_page.is_logged_in(), "Login failed"
    
    yield page


@pytest.fixture(scope="function")
def login_page(page: Page):
    """Fixture to provide LoginPage instance"""
    from utils.login_page import LoginPage
    return LoginPage(page)


@pytest.fixture(scope="function")
def dashboard_page(authenticated_page: Page):
    """Fixture to provide DashboardPage instance with authenticated user"""
    from pages.dashboard_page import DashboardPage
    dashboard = DashboardPage(authenticated_page)
    dashboard.navigate()
    return dashboard


# Hook to capture test failures for screenshot
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# Markers for different test types
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "ui: UI tests using Playwright"
    )
    config.addinivalue_line(
        "markers", "smoke: Smoke tests for critical functionality"
    )
    config.addinivalue_line(
        "markers", "regression: Regression tests"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer to execute"
    )
