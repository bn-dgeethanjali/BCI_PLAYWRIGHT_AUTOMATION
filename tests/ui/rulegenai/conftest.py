"""
RuleGen AI Test Configuration
Pytest fixtures specific to RuleGen AI testing
Credentials are loaded from config file: mcp/projects/rulegenai.yaml
"""

import os
import sys
import pytest
import yaml
import re
from playwright.sync_api import Page, BrowserContext

# Add workspace root to path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from pages.locators.rulegenai_locators import (
    RuleGenAILoginLocators,
    RuleGenAIDashboardLocators,
    RuleGenAIRuleGeneratorLocators,
    RuleGenAIRulesListLocators,
)


def load_config_from_yaml():
    """Load configuration from rulegenai.yaml config file"""
    config_path = os.path.join(workspace_root, "mcp", "projects", "rulegenai.yaml")

    if not os.path.exists(config_path):
        return {}

    with open(config_path, "r") as f:
        content = f.read()

    # Resolve environment variables with defaults: ${VAR:-default}
    def resolve_env_var(match):
        var_expr = match.group(1)
        if ":-" in var_expr:
            var_name, default = var_expr.split(":-", 1)
            return os.getenv(var_name, default)
        else:
            return os.getenv(var_expr, "")

    resolved_content = re.sub(r'\$\{([^}]+)\}', resolve_env_var, content)

    return yaml.safe_load(resolved_content)


# Load config from YAML file
_yaml_config = load_config_from_yaml()


# RuleGen AI Configuration
class RuleGenAIConfig:
    """Configuration for RuleGen AI tests - loaded from rulegenai.yaml"""

    # Load from YAML config with env var override
    BASE_URL = os.getenv("RULEGENAI_BASE_URL", _yaml_config.get("base_url", "http://rule-gen-ai.dev.bci.aws.cudaops.com"))

    # Credentials from config file (with env var override)
    _creds = _yaml_config.get("credentials", {})
    USERNAME = os.getenv("RULEGENAI_USERNAME", _creds.get("username", ""))
    PASSWORD = os.getenv("RULEGENAI_PASSWORD", _creds.get("password", ""))

    WORKSPACE_ID = os.getenv("RULEGENAI_WORKSPACE_ID", _yaml_config.get("test_data", {}).get("workspace_id", "12"))

    LOGIN_URL = f"{BASE_URL}/login"
    DASHBOARD_URL = f"{BASE_URL}/workspaces/{WORKSPACE_ID}"
    WORKSPACES_URL = f"{BASE_URL}/workspaces"
    RULES_URL = f"{BASE_URL}/workspaces/{WORKSPACE_ID}/rules"
    SETTINGS_URL = f"{BASE_URL}/settings"

    # Timeouts from config
    _browser_config = _yaml_config.get("browser", {})
    DEFAULT_TIMEOUT = int(_browser_config.get("timeout", 30000))
    GENERATION_TIMEOUT = 60000  # AI generation may take longer


@pytest.fixture(scope="module")
def rulegenai_config():
    """Provide RuleGen AI configuration"""
    return RuleGenAIConfig


@pytest.fixture(scope="function")
def rulegenai_page(page: Page) -> Page:
    """
    Provide a page configured for RuleGen AI testing.
    Sets appropriate timeout for AI operations.
    """
    page.set_default_timeout(RuleGenAIConfig.DEFAULT_TIMEOUT)
    yield page


@pytest.fixture(scope="function")
def authenticated_rulegenai_page(page: Page) -> Page:
    """
    Provide an authenticated page for RuleGen AI.
    Performs login before yielding the page.
    """
    page.set_default_timeout(RuleGenAIConfig.DEFAULT_TIMEOUT)

    # Navigate to login page
    page.goto(RuleGenAIConfig.LOGIN_URL)
    page.wait_for_load_state("networkidle")

    # Check if already logged in
    if "/login" not in page.url.lower():
        yield page
        return

    # Perform login
    username = RuleGenAIConfig.USERNAME
    password = RuleGenAIConfig.PASSWORD

    if not username or not password:
        pytest.skip("RULEGENAI_USERNAME and RULEGENAI_PASSWORD environment variables required")

    # Fill login form
    username_field = page.locator(RuleGenAILoginLocators.USERNAME_INPUT).first
    password_field = page.locator(RuleGenAILoginLocators.PASSWORD_INPUT).first
    login_button = page.locator(RuleGenAILoginLocators.LOGIN_BUTTON).first

    username_field.fill(username)
    password_field.fill(password)
    login_button.click()

    # Wait for navigation
    page.wait_for_load_state("networkidle")

    # Verify login success
    if "/login" in page.url.lower():
        error = page.locator(RuleGenAILoginLocators.ERROR_MESSAGE)
        if error.count() > 0:
            pytest.fail(f"Login failed: {error.first.text_content()}")

    yield page


@pytest.fixture(scope="function")
def dashboard_page(authenticated_rulegenai_page: Page) -> Page:
    """
    Provide a page on the RuleGen AI dashboard.
    """
    page = authenticated_rulegenai_page
    page.goto(RuleGenAIConfig.DASHBOARD_URL)
    page.wait_for_load_state("networkidle")
    yield page


# Test Data Fixtures
@pytest.fixture
def sample_prompts():
    """Sample prompts for rule generation testing"""
    return [
        "Generate a YARA rule to detect ransomware encryption patterns",
        "Create an email security rule to block phishing attempts",
        "Write a network detection rule for lateral movement",
        "Generate a rule to identify credential harvesting attempts",
    ]


@pytest.fixture
def invalid_prompts():
    """Invalid prompts for negative testing"""
    return [
        "",  # Empty
        "   ",  # Whitespace only
        "a",  # Too short
        "<script>alert('xss')</script>",  # XSS attempt
        "x" * 10001,  # Too long (if limit exists)
    ]


@pytest.fixture
def test_rule_data():
    """Test data for rule creation"""
    return {
        "name": "Test Rule - Automated",
        "description": "Rule created by automated test",
        "type": "email",
        "severity": "high",
        "tags": ["test", "automated", "ci"],
    }


# Markers
def pytest_configure(config):
    """Register custom markers for RuleGen AI tests"""
    config.addinivalue_line("markers", "rulegenai: RuleGen AI specific tests")
    config.addinivalue_line("markers", "ai_generation: Tests involving AI rule generation")
    config.addinivalue_line("markers", "workspace: Workspace management tests")
    config.addinivalue_line("markers", "rules: Rule management tests")
    config.addinivalue_line("markers", "slow: Tests that may take longer due to AI processing")
