"""
MCP Helper Utilities

Provides helper functions that work with the MCP configuration system.
These helpers can be used by tests to access configuration-driven values.
"""

import os
from typing import Any, Dict, List, Optional
from mcp.mcp_config import MCPConfig


class URLHelper:
    """Helper for constructing URLs from configuration"""

    @staticmethod
    def get_base_url() -> str:
        """Get the base URL for the current project"""
        return MCPConfig.get("base_url", "")

    @staticmethod
    def get_full_url(path: str) -> str:
        """
        Construct full URL from path.

        Args:
            path: Relative path (e.g., "/login", "api/users")

        Returns:
            Full URL with base URL prepended
        """
        base = MCPConfig.get("base_url", "").rstrip("/")
        path = path.lstrip("/")
        return f"{base}/{path}"

    @staticmethod
    def get_api_url(endpoint: str) -> str:
        """
        Get full API URL for an endpoint.

        Args:
            endpoint: Endpoint key from config or path

        Returns:
            Full API URL
        """
        api_base = MCPConfig.get("api.base_url", MCPConfig.get("base_url", ""))
        api_base = api_base.rstrip("/")

        # Check if endpoint is a config key
        endpoints = MCPConfig.get("api.endpoints", {})
        path = endpoints.get(endpoint, endpoint)

        return f"{api_base}/{path.lstrip('/')}"

    @staticmethod
    def get_tool_url(tool_name: str) -> str:
        """
        Get URL for a specific tool.

        Args:
            tool_name: Tool name (e.g., "whois", "mxlookup")

        Returns:
            Full tool URL
        """
        tools = MCPConfig.get("tools", {})
        path = tools.get(tool_name, f"/tools/{tool_name}/")
        return URLHelper.get_full_url(path)


class LocatorHelper:
    """Helper for accessing locators from configuration"""

    @staticmethod
    def get(name: str, default: Optional[str] = None) -> str:
        """
        Get locator by logical name.

        Args:
            name: Logical locator name (e.g., "login_username")
            default: Default selector if not found

        Returns:
            CSS/XPath selector string
        """
        locators = MCPConfig.get("locator_mappings", {})
        return locators.get(name, default or name)

    @staticmethod
    def get_all() -> Dict[str, str]:
        """Get all configured locator mappings"""
        return MCPConfig.get("locator_mappings", {})

    @staticmethod
    def has(name: str) -> bool:
        """Check if locator is configured"""
        locators = MCPConfig.get("locator_mappings", {})
        return name in locators


class CredentialHelper:
    """Helper for accessing credentials from configuration"""

    @staticmethod
    def get_username() -> str:
        """Get username from environment (as specified in config)"""
        credentials = MCPConfig.get("credentials", {})
        username_env = credentials.get("username_env", "USERNAME")
        return os.getenv(username_env, credentials.get("username", ""))

    @staticmethod
    def get_password() -> str:
        """Get password from environment (as specified in config)"""
        credentials = MCPConfig.get("credentials", {})
        password_env = credentials.get("password_env", "PASSWORD")
        return os.getenv(password_env, credentials.get("password", ""))

    @staticmethod
    def get_credentials() -> Dict[str, str]:
        """Get both username and password as dict"""
        return {
            "username": CredentialHelper.get_username(),
            "password": CredentialHelper.get_password()
        }


class TestDataHelper:
    """Helper for accessing test data from configuration"""

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Get test data value by key.

        Args:
            key: Dot-notation key (e.g., "default_user.username")
            default: Default value if not found

        Returns:
            Test data value
        """
        return MCPConfig.get(f"test_data.{key}", default)

    @staticmethod
    def get_test_domains() -> List[str]:
        """Get list of test domains"""
        return MCPConfig.get("test_data.test_domains", [])

    @staticmethod
    def get_test_ips() -> List[str]:
        """Get list of test IP addresses"""
        return MCPConfig.get("test_data.test_ips", [])

    @staticmethod
    def get_test_urls() -> List[str]:
        """Get list of test URLs"""
        return MCPConfig.get("test_data.test_urls", [])


class BrowserConfigHelper:
    """Helper for browser configuration"""

    @staticmethod
    def get_timeout() -> int:
        """Get default timeout in milliseconds"""
        return int(MCPConfig.get("browser.timeout", 30000))

    @staticmethod
    def get_viewport() -> Dict[str, int]:
        """Get viewport dimensions"""
        viewport = MCPConfig.get("browser.viewport", {})
        return {
            "width": int(viewport.get("width", 1920)),
            "height": int(viewport.get("height", 1080))
        }

    @staticmethod
    def is_headless() -> bool:
        """Check if running in headless mode"""
        headless = MCPConfig.get("browser.headless", True)
        if isinstance(headless, str):
            return headless.lower() in ("true", "1", "yes")
        return bool(headless)

    @staticmethod
    def get_browser_type() -> str:
        """Get browser type (chromium, firefox, webkit)"""
        return MCPConfig.get("browser.type", "chromium")


class RetryHelper:
    """Helper for retry configuration"""

    @staticmethod
    def get_max_attempts() -> int:
        """Get maximum retry attempts"""
        return int(MCPConfig.get("retry.max_attempts", 3))

    @staticmethod
    def get_delay() -> float:
        """Get retry delay in seconds"""
        return float(MCPConfig.get("retry.delay_seconds", 2))

    @staticmethod
    def get_backoff_multiplier() -> float:
        """Get backoff multiplier for exponential backoff"""
        return float(MCPConfig.get("retry.backoff_multiplier", 1.5))


def wait_with_retry(func, *args, **kwargs):
    """
    Execute function with retry logic from configuration.

    Args:
        func: Function to execute
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func

    Returns:
        Function result

    Raises:
        Last exception if all retries fail
    """
    import time

    max_attempts = RetryHelper.get_max_attempts()
    delay = RetryHelper.get_delay()
    multiplier = RetryHelper.get_backoff_multiplier()

    last_exception = None

    for attempt in range(max_attempts):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < max_attempts - 1:
                time.sleep(delay)
                delay *= multiplier

    raise last_exception
