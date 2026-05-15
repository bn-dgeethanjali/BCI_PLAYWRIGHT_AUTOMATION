"""
MCP Adapter Layer for BCI Playwright Automation Framework

This module provides a configuration-driven adapter layer that enables:
1. Playwright MCP integration without modifying existing framework
2. Multi-project support through YAML configuration files
3. Seamless fallback to local Playwright when MCP is unavailable

Usage:
    # Enable MCP mode via environment variable
    export USE_MCP=true
    export MCP_PROJECT=mailxray

    # Or use local Playwright (default)
    export USE_MCP=false
"""

from mcp.mcp_config import MCPConfig
from mcp.mcp_browser_adapter import MCPBrowserAdapter

__all__ = ['MCPConfig', 'MCPBrowserAdapter']
