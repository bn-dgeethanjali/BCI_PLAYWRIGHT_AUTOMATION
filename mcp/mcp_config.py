"""
MCP Configuration Manager

Loads project-specific configurations from YAML files.
Supports environment variable substitution and nested key access.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from functools import lru_cache


class MCPConfigError(Exception):
    """Raised when configuration loading or access fails"""
    pass


class MCPConfig:
    """
    Configuration manager for MCP adapter layer.

    Loads project-specific settings from YAML files in mcp/projects/
    Supports environment variable substitution using ${VAR:-default} syntax.

    Usage:
        # Load a specific project
        config = MCPConfig.load_project("mailxray")

        # Get values with dot notation
        base_url = MCPConfig.get("base_url")
        username_field = MCPConfig.get("locator_mappings.login_username")

        # Get with default
        timeout = MCPConfig.get("browser.timeout", 30000)
    """

    _instance = None
    _project_config: Dict[str, Any] = {}
    _project_name: str = ""
    _config_dir: Path = Path(__file__).parent / "projects"

    # Environment variable pattern: ${VAR_NAME} or ${VAR_NAME:-default_value}
    ENV_VAR_PATTERN = re.compile(r'\$\{([^}:]+)(?::-([^}]*))?\}')

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def load_project(cls, project_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Load project configuration from YAML file.

        Args:
            project_name: Name of project (matches filename in projects/).
                         Defaults to MCP_PROJECT env var or 'mailxray'.

        Returns:
            Dict containing project configuration

        Raises:
            MCPConfigError: If config file not found or invalid
        """
        project_name = project_name or os.getenv("MCP_PROJECT", "mailxray")

        # Skip reload if same project already loaded
        if cls._project_name == project_name and cls._project_config:
            return cls._project_config

        config_path = cls._config_dir / f"{project_name}.yaml"

        if not config_path.exists():
            # Try .yml extension
            config_path = cls._config_dir / f"{project_name}.yml"

        if not config_path.exists():
            raise MCPConfigError(
                f"Project config not found: {project_name}\n"
                f"Expected at: {cls._config_dir / project_name}.yaml\n"
                f"Available projects: {cls.list_projects()}"
            )

        try:
            with open(config_path, 'r') as f:
                raw_config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise MCPConfigError(f"Invalid YAML in {config_path}: {e}")

        # Resolve environment variables recursively
        cls._project_config = cls._resolve_env_vars(raw_config)
        cls._project_name = project_name

        # Clear cached values when config changes
        cls.get.cache_clear()

        return cls._project_config

    @classmethod
    @lru_cache(maxsize=128)
    def get(cls, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key_path: Dot-separated path to value (e.g., "browser.viewport.width")
            default: Value to return if key not found

        Returns:
            Configuration value or default

        Examples:
            MCPConfig.get("base_url")
            MCPConfig.get("browser.headless", True)
            MCPConfig.get("locator_mappings.login_username")
        """
        if not cls._project_config:
            cls.load_project()

        keys = key_path.split('.')
        value = cls._project_config

        try:
            for key in keys:
                if isinstance(value, dict):
                    value = value[key]
                elif isinstance(value, list) and key.isdigit():
                    value = value[int(key)]
                else:
                    return default
            return value
        except (KeyError, IndexError, TypeError):
            return default

    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """Get entire configuration dictionary"""
        if not cls._project_config:
            cls.load_project()
        return cls._project_config.copy()

    @classmethod
    def get_project_name(cls) -> str:
        """Get currently loaded project name"""
        return cls._project_name

    @classmethod
    def list_projects(cls) -> list:
        """List all available project configurations"""
        if not cls._config_dir.exists():
            return []

        projects = []
        for f in cls._config_dir.iterdir():
            if f.suffix in ('.yaml', '.yml') and f.is_file():
                projects.append(f.stem)
        return sorted(projects)

    @classmethod
    def _resolve_env_vars(cls, obj: Any) -> Any:
        """
        Recursively resolve environment variables in configuration.

        Supports syntax: ${VAR_NAME} or ${VAR_NAME:-default_value}
        """
        if isinstance(obj, str):
            def replace_env_var(match):
                var_name = match.group(1)
                default_value = match.group(2) if match.group(2) is not None else ""
                return os.getenv(var_name, default_value)

            return cls.ENV_VAR_PATTERN.sub(replace_env_var, obj)

        elif isinstance(obj, dict):
            return {k: cls._resolve_env_vars(v) for k, v in obj.items()}

        elif isinstance(obj, list):
            return [cls._resolve_env_vars(item) for item in obj]

        return obj

    @classmethod
    def reload(cls) -> Dict[str, Any]:
        """Force reload of current project configuration"""
        cls._project_config = {}
        cls.get.cache_clear()
        return cls.load_project(cls._project_name or None)

    @classmethod
    def reset(cls):
        """Reset configuration state (useful for testing)"""
        cls._project_config = {}
        cls._project_name = ""
        cls.get.cache_clear()


# Convenience function for quick access
def get_config(key: str, default: Any = None) -> Any:
    """Shortcut to MCPConfig.get()"""
    return MCPConfig.get(key, default)
