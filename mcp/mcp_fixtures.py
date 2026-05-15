"""
MCP Pytest Fixtures

Provides pytest fixtures that integrate with the MCP adapter layer.
These fixtures can replace or augment the existing Playwright fixtures
without modifying existing test code.

Usage in conftest.py:
    # Option 1: Use MCP fixtures directly
    from mcp.mcp_fixtures import *

    # Option 2: Conditional loading
    import os
    if os.getenv("USE_MCP", "false").lower() == "true":
        from mcp.mcp_fixtures import *
    else:
        from tests.ui.conftest import *
"""

import os
import pytest
import logging
from typing import Generator
from playwright.sync_api import Browser, BrowserContext, Page

from mcp.mcp_config import MCPConfig
from mcp.mcp_browser_adapter import MCPBrowserAdapter

logger = logging.getLogger(__name__)


# Store adapter at module level for session scope
_adapter: MCPBrowserAdapter = None


def get_adapter() -> MCPBrowserAdapter:
    """Get or create the global adapter instance"""
    global _adapter
    if _adapter is None:
        _adapter = MCPBrowserAdapter()
    return _adapter


@pytest.fixture(scope="session")
def mcp_config():
    """
    Session-scoped fixture providing project configuration.

    Usage:
        def test_example(mcp_config):
            base_url = mcp_config.get("base_url")
    """
    config = MCPConfig.load_project()
    logger.info(f"Loaded MCP config for project: {MCPConfig.get_project_name()}")
    return MCPConfig


@pytest.fixture(scope="session")
def mcp_adapter(mcp_config) -> Generator[MCPBrowserAdapter, None, None]:
    """
    Session-scoped fixture providing the MCP browser adapter.

    The adapter manages browser lifecycle and provides unified access
    to browser instances whether from MCP or local Playwright.
    """
    adapter = get_adapter()
    yield adapter
    adapter.cleanup()
    global _adapter
    _adapter = None


@pytest.fixture(scope="session")
def browser(mcp_adapter: MCPBrowserAdapter) -> Generator[Browser, None, None]:
    """
    Session-scoped browser fixture.

    This replaces the standard Playwright browser fixture.
    Tests using this fixture work identically whether MCP is enabled or not.

    Usage:
        def test_example(browser):
            context = browser.new_context()
            page = context.new_page()
    """
    browser = mcp_adapter.get_browser()
    use_mcp = os.getenv("USE_MCP", "false").lower() in ("true", "1", "yes")
    logger.info(f"Browser ready (MCP: {use_mcp})")
    yield browser
    # Cleanup handled by mcp_adapter fixture


@pytest.fixture(scope="function")
def context(browser: Browser, mcp_adapter: MCPBrowserAdapter) -> Generator[BrowserContext, None, None]:
    """
    Function-scoped browser context fixture.

    Creates a fresh context for each test with project-specific configuration.

    Usage:
        def test_example(context):
            page = context.new_page()
            page.goto("/")
    """
    context = mcp_adapter.create_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Function-scoped page fixture.

    Provides a fresh page for each test. This is the primary fixture
    most tests will use.

    Usage:
        def test_login(page):
            page.goto("/login")
            page.fill("#username", "user")
    """
    page = context.new_page()

    # Apply timeout from config
    timeout = MCPConfig.get("browser.timeout", 30000)
    page.set_default_timeout(int(timeout))

    yield page
    page.close()


@pytest.fixture(scope="function")
def authenticated_page(page: Page) -> Generator[Page, None, None]:
    """
    Function-scoped fixture providing a logged-in page.

    Performs login using credentials from project configuration
    before yielding the page to the test.

    Usage:
        def test_dashboard(authenticated_page):
            # Already logged in
            authenticated_page.goto("/dashboard")
    """
    # Get login configuration
    login_url = MCPConfig.get("login_url", "/accounts/login/")
    base_url = MCPConfig.get("base_url", "")

    # Get credentials from config (which reads from env vars)
    credentials = MCPConfig.get("credentials", {})
    username_env = credentials.get("username_env", "USERNAME")
    password_env = credentials.get("password_env", "PASSWORD")

    username = os.getenv(username_env, credentials.get("username", ""))
    password = os.getenv(password_env, credentials.get("password", ""))

    # Get locators from config
    locators = MCPConfig.get("locator_mappings", {})
    username_selector = locators.get("login_username", "input[name='username']")
    password_selector = locators.get("login_password", "input[type='password']")
    login_button_selector = locators.get("login_button", "button[type='submit']")

    # Perform login
    full_login_url = f"{base_url.rstrip('/')}/{login_url.lstrip('/')}"
    page.goto(full_login_url)
    page.wait_for_load_state("networkidle")

    page.fill(username_selector, username)
    page.fill(password_selector, password)
    page.click(login_button_selector)
    page.wait_for_load_state("networkidle")

    # Verify login success
    success_indicator = MCPConfig.get("login_success_indicator", {})
    if success_indicator:
        if "url_contains" in success_indicator:
            assert success_indicator["url_contains"] in page.url, "Login failed - URL check"
        if "element_visible" in success_indicator:
            assert page.locator(success_indicator["element_visible"]).is_visible(), "Login failed - element check"

    logger.info(f"Authenticated as user from {username_env}")
    yield page


@pytest.fixture(scope="function")
def api_base_url(mcp_config) -> str:
    """
    Fixture providing the API base URL from configuration.

    Usage:
        def test_api(api_base_url):
            response = requests.get(f"{api_base_url}/endpoint")
    """
    return MCPConfig.get("api.base_url", MCPConfig.get("base_url", ""))


@pytest.fixture(scope="function")
def test_data(mcp_config) -> dict:
    """
    Fixture providing test data from configuration.

    Usage:
        def test_with_data(test_data):
            user = test_data.get("default_user")
    """
    return MCPConfig.get("test_data", {})


# Screenshot on failure hook
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshots on test failure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Check if screenshot on failure is enabled
        if MCPConfig.get("browser.screenshot_on_failure", True):
            try:
                page = item.funcargs.get("page") or item.funcargs.get("authenticated_page")
                if page:
                    screenshot_dir = MCPConfig.get("browser.screenshots_dir", "screenshots")
                    os.makedirs(screenshot_dir, exist_ok=True)
                    screenshot_path = os.path.join(
                        screenshot_dir,
                        f"failure_{item.name}_{rep.when}.png"
                    )
                    page.screenshot(path=screenshot_path, full_page=True)
                    logger.info(f"Failure screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Failed to capture screenshot: {e}")


# Custom markers registration
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "mcp: Tests that specifically require MCP")
    config.addinivalue_line("markers", "local_only: Tests that should skip when MCP is enabled")
    config.addinivalue_line("markers", "smoke: Smoke tests for critical functionality")
    config.addinivalue_line("markers", "regression: Regression tests")


# Skip markers based on MCP mode
def pytest_collection_modifyitems(config, items):
    """Modify test collection based on MCP mode"""
    use_mcp = os.getenv("USE_MCP", "false").lower() in ("true", "1", "yes")

    skip_mcp = pytest.mark.skip(reason="Test requires MCP mode")
    skip_local = pytest.mark.skip(reason="Test skipped in MCP mode")

    for item in items:
        if "mcp" in item.keywords and not use_mcp:
            item.add_marker(skip_mcp)
        if "local_only" in item.keywords and use_mcp:
            item.add_marker(skip_local)
