"""
MCP Browser Adapter

Provides a unified interface for browser automation that works with both:
1. Playwright MCP (remote browser via MCP protocol)
2. Local Playwright (fallback when MCP unavailable)

The adapter ensures that the browser/context/page objects returned are
compatible with the existing framework, requiring no changes to tests.
"""

import os
import logging
from typing import Any, Dict, Optional, Union
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright

from mcp.mcp_config import MCPConfig

logger = logging.getLogger(__name__)


class MCPBrowserAdapter:
    """
    Adapter that provides browser instances from MCP or local Playwright.

    This adapter abstracts the browser source, allowing tests to work
    identically whether using MCP or local Playwright.

    Usage:
        adapter = MCPBrowserAdapter()
        browser = adapter.get_browser()
        context = adapter.create_context()
        page = adapter.create_page()

        # When done
        adapter.cleanup()
    """

    def __init__(self, project_name: Optional[str] = None):
        """
        Initialize the browser adapter.

        Args:
            project_name: Optional project name to load config for.
                         Uses MCP_PROJECT env var if not specified.
        """
        self.config = MCPConfig.load_project(project_name)
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._contexts: list = []
        self._mcp_client = None
        self._use_mcp = self._should_use_mcp()

    def _should_use_mcp(self) -> bool:
        """Determine whether to use MCP or local Playwright"""
        use_mcp_env = os.getenv("USE_MCP", "false").lower()
        use_mcp_config = MCPConfig.get("mcp.enabled", False)
        return use_mcp_env in ("true", "1", "yes") or use_mcp_config

    def _get_browser_config(self) -> Dict[str, Any]:
        """Get browser launch configuration from project config"""
        browser_config = MCPConfig.get("browser", {})

        # Default configuration
        config = {
            "headless": self._parse_bool(browser_config.get("headless", True)),
            "slow_mo": int(browser_config.get("slow_mo", 0)),
            "args": browser_config.get("args", [
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ])
        }

        # Add any additional launch options
        if "launch_options" in browser_config:
            config.update(browser_config["launch_options"])

        return config

    def _get_context_config(self) -> Dict[str, Any]:
        """Get browser context configuration from project config"""
        browser_config = MCPConfig.get("browser", {})

        viewport = browser_config.get("viewport", {})
        if isinstance(viewport, dict):
            viewport_config = {
                "width": int(viewport.get("width", 1920)),
                "height": int(viewport.get("height", 1080))
            }
        else:
            viewport_config = {"width": 1920, "height": 1080}

        config = {
            "viewport": viewport_config,
            "ignore_https_errors": browser_config.get("ignore_https_errors", True),
            "base_url": MCPConfig.get("base_url"),
        }

        # Video recording
        if browser_config.get("record_video", False):
            config["record_video_dir"] = browser_config.get("video_dir", "videos")

        # Additional context options
        if "context_options" in browser_config:
            config.update(browser_config["context_options"])

        return config

    def _parse_bool(self, value: Any) -> bool:
        """Parse boolean from various formats"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "on")
        return bool(value)

    def connect(self) -> Browser:
        """
        Connect to browser (MCP or local).

        Returns:
            Browser instance ready for use
        """
        if self._browser:
            return self._browser

        if self._use_mcp:
            self._browser = self._connect_mcp()
        else:
            self._browser = self._connect_local()

        return self._browser

    def _connect_mcp(self) -> Browser:
        """
        Connect to Playwright MCP server.

        This method connects to an external Playwright MCP server
        that provides browser automation over the MCP protocol.
        """
        mcp_config = MCPConfig.get("mcp", {})
        server_url = mcp_config.get("server_url", os.getenv("MCP_SERVER_URL"))

        if not server_url:
            logger.warning("MCP server URL not configured, falling back to local Playwright")
            return self._connect_local()

        try:
            # Import MCP client library
            # Note: This assumes @anthropic-ai/mcp or similar is available
            from mcp import ClientSession
            from mcp.client.stdio import stdio_client

            logger.info(f"Connecting to Playwright MCP at {server_url}")

            # Connect to MCP server
            # The actual implementation depends on how Playwright MCP is exposed
            # This is a placeholder for the MCP connection logic

            # For now, we'll use a CDP connection if available
            if "cdp_endpoint" in mcp_config:
                self._playwright = sync_playwright().start()
                self._browser = self._playwright.chromium.connect_over_cdp(
                    mcp_config["cdp_endpoint"]
                )
                logger.info("Connected to browser via CDP endpoint")
                return self._browser

            # If MCP client available, use it
            # This would integrate with the actual Playwright MCP server
            raise NotImplementedError(
                "Direct MCP connection not yet implemented. "
                "Please configure cdp_endpoint or use local Playwright."
            )

        except ImportError:
            logger.warning("MCP client library not available, falling back to local Playwright")
            return self._connect_local()
        except Exception as e:
            logger.error(f"MCP connection failed: {e}, falling back to local Playwright")
            return self._connect_local()

    def _connect_local(self) -> Browser:
        """Connect to local Playwright browser"""
        browser_type = MCPConfig.get("browser.type", "chromium")
        browser_config = self._get_browser_config()

        logger.info(f"Launching local {browser_type} browser")

        self._playwright = sync_playwright().start()

        browser_launcher = getattr(self._playwright, browser_type, self._playwright.chromium)
        self._browser = browser_launcher.launch(**browser_config)

        return self._browser

    def get_browser(self) -> Browser:
        """Get browser instance, connecting if necessary"""
        if not self._browser:
            self.connect()
        return self._browser

    def create_context(self, **kwargs) -> BrowserContext:
        """
        Create a new browser context with project configuration.

        Args:
            **kwargs: Additional context options (override config)

        Returns:
            BrowserContext instance
        """
        browser = self.get_browser()

        # Merge config with overrides
        context_config = self._get_context_config()
        context_config.update(kwargs)

        context = browser.new_context(**context_config)

        # Set default timeout
        timeout = MCPConfig.get("browser.timeout", 30000)
        context.set_default_timeout(int(timeout))

        self._contexts.append(context)
        return context

    def create_page(self, context: Optional[BrowserContext] = None) -> Page:
        """
        Create a new page, optionally in an existing context.

        Args:
            context: Existing context to use. Creates new one if None.

        Returns:
            Page instance
        """
        if context is None:
            context = self.create_context()

        page = context.new_page()

        # Apply page-level settings
        timeout = MCPConfig.get("browser.timeout", 30000)
        page.set_default_timeout(int(timeout))

        return page

    def cleanup(self):
        """Clean up all browser resources"""
        # Close all contexts
        for context in self._contexts:
            try:
                context.close()
            except Exception as e:
                logger.warning(f"Error closing context: {e}")
        self._contexts.clear()

        # Close browser
        if self._browser:
            try:
                self._browser.close()
            except Exception as e:
                logger.warning(f"Error closing browser: {e}")
            self._browser = None

        # Stop playwright
        if self._playwright:
            try:
                self._playwright.stop()
            except Exception as e:
                logger.warning(f"Error stopping playwright: {e}")
            self._playwright = None

        # Close MCP client
        if self._mcp_client:
            try:
                self._mcp_client.close()
            except Exception as e:
                logger.warning(f"Error closing MCP client: {e}")
            self._mcp_client = None

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
        return False

    @property
    def is_mcp(self) -> bool:
        """Check if using MCP connection"""
        return self._use_mcp and self._mcp_client is not None

    @property
    def is_connected(self) -> bool:
        """Check if browser is connected"""
        return self._browser is not None and self._browser.is_connected()


class MCPPageWrapper:
    """
    Wrapper for Page that adds MCP-specific functionality.

    This wrapper can intercept page operations and add logging,
    screenshots, or other cross-cutting concerns without modifying tests.
    """

    def __init__(self, page: Page, config: Dict[str, Any]):
        self._page = page
        self._config = config
        self._action_count = 0

    def __getattr__(self, name: str):
        """Delegate attribute access to wrapped page"""
        return getattr(self._page, name)

    def goto(self, url: str, **kwargs):
        """Navigate to URL with optional base URL resolution"""
        base_url = self._config.get("base_url", "")

        # If URL is relative and base_url is configured, prepend it
        if not url.startswith(("http://", "https://", "file://")) and base_url:
            url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"

        logger.debug(f"Navigating to: {url}")
        return self._page.goto(url, **kwargs)

    def click(self, selector: str, **kwargs):
        """Click with optional selector mapping"""
        mapped_selector = self._map_selector(selector)
        logger.debug(f"Clicking: {mapped_selector}")
        return self._page.click(mapped_selector, **kwargs)

    def fill(self, selector: str, value: str, **kwargs):
        """Fill with optional selector mapping"""
        mapped_selector = self._map_selector(selector)
        logger.debug(f"Filling: {mapped_selector}")
        return self._page.fill(mapped_selector, value, **kwargs)

    def _map_selector(self, selector: str) -> str:
        """Map selector aliases to actual selectors from config"""
        locator_mappings = self._config.get("locator_mappings", {})
        return locator_mappings.get(selector, selector)
