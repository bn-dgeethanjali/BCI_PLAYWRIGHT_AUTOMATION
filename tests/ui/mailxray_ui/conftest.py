"""Conftest for mailxray UI tests."""
import pytest
import sys
import os

# Add workspace root to path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)


@pytest.fixture
def page(browser):
    """Provide a new page for each test."""
    from resources.playwright_config import PlaywrightConfig
    
    PlaywrightConfig.ensure_directories()
    context = browser.new_context(**PlaywrightConfig.get_context_config())
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="session")
def browser():
    """Session-scoped browser instance."""
    from playwright.sync_api import sync_playwright
    from resources.playwright_config import PlaywrightConfig
    
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, PlaywrightConfig.BROWSER)
        browser = browser_type.launch(**PlaywrightConfig.get_browser_config())
        yield browser
        browser.close()
