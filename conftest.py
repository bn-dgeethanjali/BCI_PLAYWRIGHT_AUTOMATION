"""
Root-level pytest configuration

This conftest.py provides automatic switching between:
1. MCP mode - Uses Playwright via MCP protocol (when USE_MCP=true)
2. Local mode - Uses standard local Playwright (default)

Usage:
    # Run with local Playwright (default)
    pytest tests/

    # Run with MCP
    USE_MCP=true pytest tests/

    # Run with specific project config
    MCP_PROJECT=mailxray USE_MCP=true pytest tests/
"""

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# Determine which fixtures to use based on USE_MCP environment variable
USE_MCP = os.getenv("USE_MCP", "false").lower() in ("true", "1", "yes")

if USE_MCP:
    # Import MCP fixtures - these override standard Playwright fixtures
    from mcp.mcp_fixtures import (
        mcp_config,
        mcp_adapter,
        browser,
        context,
        page,
        authenticated_page,
        api_base_url,
        test_data,
        pytest_runtest_makereport,
        pytest_configure,
        pytest_collection_modifyitems,
    )

    print(f"[MCP MODE] Loading fixtures from mcp.mcp_fixtures")
    print(f"[MCP MODE] Project: {os.getenv('MCP_PROJECT', 'mailxray')}")

else:
    # Import standard fixtures from existing conftest
    # This maintains full backward compatibility
    from tests.ui.conftest import (
        browser,
        context,
        page,
        authenticated_page,
        login_page,
        dashboard_page,
        pytest_runtest_makereport,
        pytest_configure,
    )

    print("[LOCAL MODE] Loading fixtures from tests.ui.conftest")


# Common fixtures available in both modes

import pytest


@pytest.fixture(scope="session")
def project_root_path():
    """Provide project root path"""
    return project_root


@pytest.fixture(scope="session")
def testdata_path():
    """Provide path to testdata directory"""
    return os.path.join(project_root, "testdata")


@pytest.fixture(scope="session")
def reports_path():
    """Provide path to reports directory"""
    reports_dir = os.path.join(project_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir


# Environment info fixture
@pytest.fixture(scope="session")
def env_info():
    """Provide environment information for debugging"""
    return {
        "use_mcp": USE_MCP,
        "project": os.getenv("MCP_PROJECT", "mailxray"),
        "base_url": os.getenv("BASE_URL", ""),
        "headless": os.getenv("HEADLESS", "true"),
        "browser": os.getenv("BROWSER", "chromium"),
    }


# Print test configuration at session start
def pytest_sessionstart(session):
    """Print configuration info at test session start"""
    print("\n" + "=" * 60)
    print("BCI Playwright Automation Framework")
    print("=" * 60)
    print(f"Mode: {'MCP' if USE_MCP else 'Local Playwright'}")
    print(f"Project: {os.getenv('MCP_PROJECT', 'mailxray')}")
    print(f"Base URL: {os.getenv('BASE_URL', 'Not set')}")
    print(f"Headless: {os.getenv('HEADLESS', 'true')}")
    print("=" * 60 + "\n")
