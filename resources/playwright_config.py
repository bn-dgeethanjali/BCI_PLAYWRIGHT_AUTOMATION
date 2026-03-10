import os
from typing import Dict, Any


class PlaywrightConfig:
    """Playwright configuration settings"""
    
    # Base configuration
    BASE_URL = os.getenv("BASE_URL", "https://mailxray.barracudabrts.com")
    HEADLESS = os.getenv("HEADLESS", "true").lower() not in ["false", "0", "no", "off"]
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # Slow down operations by N milliseconds
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))  # 30 seconds default
    
    # Browser configuration
    BROWSER = os.getenv("BROWSER", "chromium")  # chromium, firefox, or webkit
    VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "1080"))
    
    # Screenshot and video settings
    SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR", "screenshots")
    VIDEOS_DIR = os.getenv("VIDEOS_DIR", "videos")
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    VIDEO_ENABLED = os.getenv("VIDEO_ENABLED", "false").lower() == "true"
    
    # Retry and wait settings
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
    WAIT_AFTER_ACTION = int(os.getenv("WAIT_AFTER_ACTION", "500"))  # milliseconds
    
    # Authentication
    TEST_USERNAME = os.getenv("TEST_USERNAME", "testuser")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "testpassword")
    AUTH_TOKEN = os.getenv("MAILXRAY_AUTH_TOKEN", "3a53bb5df78e89d0eff67148b3ea723b49011788")
    
    @classmethod
    def get_browser_config(cls) -> Dict[str, Any]:
        """Get browser launch configuration"""
        return {
            "headless": cls.HEADLESS,
            "slow_mo": cls.SLOW_MO,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ]
        }
    
    @classmethod
    def get_context_config(cls) -> Dict[str, Any]:
        """Get browser context configuration"""
        config = {
            "viewport": {
                "width": cls.VIEWPORT_WIDTH,
                "height": cls.VIEWPORT_HEIGHT
            },
            "base_url": cls.BASE_URL,
            "ignore_https_errors": True,
            "record_video_dir": cls.VIDEOS_DIR if cls.VIDEO_ENABLED else None,
        }
        return config
    
    @classmethod
    def get_page_config(cls) -> Dict[str, Any]:
        """Get page configuration"""
        return {
            "timeout": cls.TIMEOUT
        }
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        os.makedirs(cls.SCREENSHOTS_DIR, exist_ok=True)
        if cls.VIDEO_ENABLED:
            os.makedirs(cls.VIDEOS_DIR, exist_ok=True)
