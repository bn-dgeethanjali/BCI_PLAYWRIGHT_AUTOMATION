# config.py
# Global configuration for UI tests

import os
from pathlib import Path
from dotenv import load_dotenv
import base64


# Load environment variables from .env and resources/env/qa.env
from dotenv import load_dotenv
env_paths = [
    Path(__file__).parent.parent / '.env',
    Path(__file__).parent.parent / 'resources' / 'env' / 'qa.env'
]
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)

# Read from environment variables
BASE_URL = os.getenv("BASE_URL", "https://mailxray.barracudabrts.com")
USERNAME = os.getenv("USERNAME")
raw_password = os.getenv("PASSWORD")
# Decode base64 password if it looks encoded
if raw_password and all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in raw_password) and '@' not in raw_password:
    try:
        PASSWORD = base64.b64decode(raw_password).decode('utf-8')
    except Exception:
        PASSWORD = raw_password
else:
    PASSWORD = raw_password
# Path fragment or regex to assert post-login success (e.g., /home or /dashboard)
LOGIN_SUCCESS_PATH = os.getenv("LOGIN_SUCCESS_PATH", "/dashboard")

# Validate required credentials are set
if not USERNAME or not PASSWORD:
    raise ValueError(
        "USERNAME and PASSWORD must be set in .env file or as environment variables. "
        "Create a .env file in the project root with:\n"
        "USERNAME=your_username\n"
        "PASSWORD=your_password"
    )
