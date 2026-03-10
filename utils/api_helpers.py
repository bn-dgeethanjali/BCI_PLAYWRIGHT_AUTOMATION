"""
API Test Helpers and Utilities
Provides reusable functions for API testing with requests library
"""
import os
import json
import requests
from typing import Dict, Any, Optional, Union, List
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from datetime import datetime
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIConfig:
    """API Test Configuration"""
    # Base URLs
    BASE_URL = os.getenv("API_BASE_URL", "https://mailxray.dev.bci.aws.cudaops.com")
    MAILXRAY_BASE_URL = os.getenv("MAILXRAY_BASE_URL", "https://mailxray.dev.bci.aws.cudaops.com")
    # Authentication (prefer .env or config.py)
    try:
        from utils.config import USERNAME as ENV_USERNAME, PASSWORD as ENV_PASSWORD, BASE_URL as ENV_BASE_URL
        USERNAME = ENV_USERNAME
        PASSWORD = ENV_PASSWORD
        BASE_URL = ENV_BASE_URL
    except Exception:
        USERNAME = os.getenv("API_USERNAME", "")
        PASSWORD = os.getenv("API_PASSWORD", "")
    API_KEY = os.getenv("API_KEY", "")
    
    # Timeouts (seconds)
    DEFAULT_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    LONG_TIMEOUT = int(os.getenv("API_LONG_TIMEOUT", "60"))
    
    # Retry settings
    MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.getenv("API_RETRY_DELAY", "2"))
    
    # Headers
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Endpoints
    ENDPOINTS = {
        "login": "/api/v1/login/",
        "whois": "/api/v1/whois/",
        "mxlookup": "/api/v1/mxlookup/",
        "virustotal_ip": "/api/v1/virustotal/ip/",
        "virustotal_url": "/api/v1/virustotal/url/",
        "virustotal_ip_report": "/api/v1/virustotal/ip/report/",
        "emldata": "/api/v1/emldata/",
        "mxblocklist": "/api/v1/mxblocklist/ip/",
        "phaas": "/api/v1/phaas/"
    }


class APIClient:
    """
    API Client for making HTTP requests
    Provides methods for all HTTP verbs with authentication, logging, and error handling
    """
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None
    ):
        """
        Initialize API Client
        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or APIConfig.BASE_URL
        self.timeout = timeout or APIConfig.DEFAULT_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update(APIConfig.DEFAULT_HEADERS)
        self.auth_token = self._fetch_auth_token()
        if self.auth_token:
            self.session.headers.update({"Authorization": f"Token {self.auth_token}"})

    def _fetch_auth_token(self) -> Optional[str]:
        """Dynamically fetch a fresh auth token from the login API using config credentials."""
        login_url = f"{self.base_url}/tools/api/login/"
        payload = {"username": APIConfig.USERNAME, "password": APIConfig.PASSWORD}
        headers = {"Content-Type": "application/json"}
        try:
            resp = requests.post(login_url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            if "token" in data:
                return data["token"]
            if "data" in data and "token" in data["data"]:
                return data["data"]["token"]
        except Exception as e:
            logger.error(f"Failed to fetch auth token: {e}")
        return None
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make GET request
        
        Args:
            endpoint: API endpoint (relative to base_url)
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional requests arguments
            
        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        timeout = timeout or self.timeout
        
        logger.info(f"GET {url}")
        logger.debug(f"Params: {params}")
        
        response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        
        self._log_response(response)
        return response
    
    def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make POST request
        
        Args:
            endpoint: API endpoint
            data: Form data or raw data
            json_data: JSON data
            files: Files to upload
            headers: Additional headers
            timeout: Request timeout
            **kwargs: Additional requests arguments
            
        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        timeout = timeout or self.timeout
        
        logger.info(f"POST {url}")
        logger.debug(f"Data: {data or json_data}")
        
        response = self.session.post(
            url,
            data=data,
            json=json_data,
            files=files,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        
        self._log_response(response)
        return response
    
    def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """Make PUT request"""
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        timeout = timeout or self.timeout
        
        logger.info(f"PUT {url}")
        
        response = self.session.put(
            url,
            data=data,
            json=json_data,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        
        self._log_response(response)
        return response
    
    def patch(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """Make PATCH request"""
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        timeout = timeout or self.timeout
        
        logger.info(f"PATCH {url}")
        
        response = self.session.patch(
            url,
            data=data,
            json=json_data,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        
        self._log_response(response)
        return response
    
    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> requests.Response:
        """Make DELETE request"""
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        timeout = timeout or self.timeout
        
        logger.info(f"DELETE {url}")
        
        response = self.session.delete(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        
        self._log_response(response)
        return response
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    
    def _merge_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Merge additional headers with session headers"""
        merged = self.session.headers.copy()
        if headers:
            merged.update(headers)
        return merged
    
    def _log_response(self, response: requests.Response) -> None:
        """Log response details"""
        logger.info(f"Response: {response.status_code} {response.reason}")
        logger.debug(f"Response body: {response.text[:500]}")  # First 500 chars
    
    def close(self):
        """Close session"""
        self.session.close()


class ResponseValidator:
    """Validate API responses"""
    
    @staticmethod
    def validate_status_code(
        response: requests.Response,
        expected_status: Union[int, List[int]]
    ) -> bool:
        """
        Validate response status code
        
        Args:
            response: Response object
            expected_status: Expected status code(s)
            
        Returns:
            True if status matches, False otherwise
        """
        if isinstance(expected_status, int):
            expected_status = [expected_status]
        
        is_valid = response.status_code in expected_status
        
        if not is_valid:
            logger.error(f"Expected status {expected_status}, got {response.status_code}")
        
        return is_valid
    
    @staticmethod
    def validate_json_response(response: requests.Response) -> bool:
        """Validate that response is valid JSON"""
        try:
            response.json()
            return True
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}")
            return False
    
    @staticmethod
    def validate_response_time(
        response: requests.Response,
        max_time: float
    ) -> bool:
        """
        Validate response time
        
        Args:
            response: Response object
            max_time: Maximum acceptable response time (seconds)
            
        Returns:
            True if within limit, False otherwise
        """
        response_time = response.elapsed.total_seconds()
        is_valid = response_time <= max_time
        
        if not is_valid:
            logger.warning(f"Response time {response_time}s exceeds {max_time}s")
        
        return is_valid
    
    @staticmethod
    def validate_schema(
        response: requests.Response,
        required_fields: List[str]
    ) -> bool:
        """
        Validate that response JSON contains required fields
        
        Args:
            response: Response object
            required_fields: List of required field names
            
        Returns:
            True if all fields present, False otherwise
        """
        try:
            data = response.json()
            
            for field in required_fields:
                if field not in data:
                    logger.error(f"Required field '{field}' not in response")
                    return False
            
            return True
        
        except json.JSONDecodeError:
            logger.error("Cannot validate schema - invalid JSON")
            return False
    
    @staticmethod
    def validate_field_value(
        response: requests.Response,
        field_name: str,
        expected_value: Any
    ) -> bool:
        """
        Validate specific field value in response
        
        Args:
            response: Response object
            field_name: Field name to check
            expected_value: Expected value
            
        Returns:
            True if value matches, False otherwise
        """
        try:
            data = response.json()
            actual_value = data.get(field_name)
            
            is_valid = actual_value == expected_value
            
            if not is_valid:
                logger.error(f"Field '{field_name}': expected {expected_value}, got {actual_value}")
            
            return is_valid
        
        except json.JSONDecodeError:
            logger.error("Cannot validate field - invalid JSON")
            return False


class AuthHelper:
    """Authentication helpers"""
    
    @staticmethod
    def get_token_auth_header(token: str) -> Dict[str, str]:
        """Get header for token authentication"""
        return {"Authorization": f"Token {token}"}
    
    @staticmethod
    def get_bearer_auth_header(token: str) -> Dict[str, str]:
        """Get header for bearer authentication"""
        return {"Authorization": f"Bearer {token}"}
    
    @staticmethod
    def get_api_key_header(api_key: str, header_name: str = "X-API-Key") -> Dict[str, str]:
        """Get header for API key authentication"""
        return {header_name: api_key}
    
    @staticmethod
    def get_basic_auth(username: str, password: str) -> HTTPBasicAuth:
        """Get basic authentication"""
        return HTTPBasicAuth(username, password)
    
    @staticmethod
    def get_digest_auth(username: str, password: str) -> HTTPDigestAuth:
        """Get digest authentication"""
        return HTTPDigestAuth(username, password)


class FileUploadHelper:
    """Helper for file uploads"""
    
    @staticmethod
    def prepare_file_upload(
        file_path: str,
        field_name: str = "file",
        mime_type: Optional[str] = None
    ) -> Dict[str, tuple]:
        """
        Prepare file for upload
        
        Args:
            file_path: Path to file
            field_name: Form field name
            mime_type: MIME type (optional)
            
        Returns:
            Files dict for requests
        """
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        if mime_type:
            return {field_name: (filename, file_content, mime_type)}
        else:
            return {field_name: (filename, file_content)}
    
    @staticmethod
    def prepare_multiple_files(
        file_paths: List[str],
        field_name: str = "files"
    ) -> List[tuple]:
        """Prepare multiple files for upload"""
        files = []
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            with open(file_path, 'rb') as f:
                files.append((field_name, (filename, f.read())))
        return files


class RequestLogger:
    """Log API requests and responses"""
    
    def __init__(self, log_dir: str = "api_logs"):
        """Initialize logger with log directory"""
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
    
    def log_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        data: Optional[Any] = None
    ) -> str:
        """
        Log API request
        
        Returns:
            Log file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        log_file = os.path.join(self.log_dir, f"request_{timestamp}.json")
        
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "url": url,
            "headers": headers,
            "params": params,
            "data": data
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return log_file
    
    def log_response(
        self,
        response: requests.Response,
        request_log_file: Optional[str] = None
    ) -> str:
        """
        Log API response
        
        Returns:
            Log file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        log_file = os.path.join(self.log_dir, f"response_{timestamp}.json")
        
        try:
            response_body = response.json()
        except:
            response_body = response.text
        
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "status_code": response.status_code,
            "reason": response.reason,
            "headers": dict(response.headers),
            "body": response_body,
            "response_time": response.elapsed.total_seconds(),
            "request_log": request_log_file
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return log_file


class APITestHelper:
    """High-level helper functions for API testing"""
    
    @staticmethod
    def assert_status_code(response: requests.Response, expected: int):
        """Assert response status code"""
        assert response.status_code == expected, \
            f"Expected status {expected}, got {response.status_code}. Response: {response.text}"
    
    @staticmethod
    def assert_success(response: requests.Response):
        """Assert successful response (2xx)"""
        assert 200 <= response.status_code < 300, \
            f"Expected success status, got {response.status_code}. Response: {response.text}"
    
    @staticmethod
    def assert_json_field(response: requests.Response, field: str, expected_value: Any):
        """Assert specific field value in JSON response"""
        data = response.json()
        assert field in data, f"Field '{field}' not in response"
        assert data[field] == expected_value, \
            f"Field '{field}': expected {expected_value}, got {data[field]}"
    
    @staticmethod
    def assert_json_contains(response: requests.Response, expected_data: Dict[str, Any]):
        """Assert response JSON contains expected key-value pairs"""
        data = response.json()
        for key, value in expected_data.items():
            assert key in data, f"Key '{key}' not in response"
            assert data[key] == value, f"Key '{key}': expected {value}, got {data[key]}"
    
    @staticmethod
    def assert_response_time(response: requests.Response, max_seconds: float):
        """Assert response time within limit"""
        response_time = response.elapsed.total_seconds()
        assert response_time <= max_seconds, \
            f"Response time {response_time}s exceeds {max_seconds}s"
    
    @staticmethod
    def get_json_value(response: requests.Response, key_path: str, default: Any = None) -> Any:
        """
        Get value from JSON response using dot notation
        
        Args:
            response: Response object
            key_path: Dot-separated key path (e.g., "user.name")
            default: Default value if key not found
            
        Returns:
            Value at key path or default
        """
        try:
            data = response.json()
            keys = key_path.split('.')
            
            for key in keys:
                data = data[key]
            
            return data
        
        except (KeyError, TypeError, json.JSONDecodeError):
            return default


# Convenience function for quick API client creation
def create_api_client(
    base_url: Optional[str] = None,
    auth_token: Optional[str] = None
) -> APIClient:
    """
    Create API client with default configuration
    
    Args:
        base_url: Base URL (optional)
        auth_token: Auth token (optional)
        
    Returns:
        APIClient instance
    """
    return APIClient(base_url=base_url, auth_token=auth_token)
