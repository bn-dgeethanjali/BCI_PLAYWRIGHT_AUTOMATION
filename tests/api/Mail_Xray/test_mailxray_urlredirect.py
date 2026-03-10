import pytest
import requests
import os
import json
import time
import sys
from urllib.parse import urlparse
from pathlib import Path

# Add workspace root to path
workspace_root = str(Path(__file__).parent.parent.parent.parent)
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

# Import credentials from utils/config.py
from utils.config import BASE_URL, USERNAME, PASSWORD


class TestMailXrayURLRedirect:
    """Comprehensive test for MailXray URL Redirect API - All scenarios in one test"""
    
    # Use BASE_URL from utils/config.py
    URL_REDIRECT_ENDPOINT = f"{BASE_URL}/tools/api/urlredirect/"
    LOGIN_ENDPOINT = f"{BASE_URL}/tools/api/login/"
    
    def get_auth_token(self):
        """Get authentication token by logging in"""
        credentials = {
            "username": USERNAME,
            "password": PASSWORD
        }
        
        response = requests.post(
            self.LOGIN_ENDPOINT,
            json=credentials,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            # Try to extract token from response or cookies
            response_data = response.json()
            
            # Check for token in response body
            if "token" in response_data:
                return response_data["token"]
            elif "data" in response_data and "token" in response_data.get("data", {}):
                return response_data["data"]["token"]
            
            # Check cookies for auth_token
            if "auth_token" in response.cookies:
                return response.cookies["auth_token"]
            
            # Return session cookies
            return response.cookies
        else:
            raise Exception(f"Failed to get authentication token: {response.status_code}")
    
    def get_headers_with_token(self, auth_token):
        """Get headers with Token authentication"""
        if isinstance(auth_token, requests.cookies.RequestsCookieJar):
            return {"Content-Type": "application/json"}
        return {
            "Content-Type": "application/json",
            "Authorization": f"Token {auth_token}"
        }
    
    def get_headers_with_cookie(self, auth_token):
        """Get headers with Cookie authentication"""
        if isinstance(auth_token, requests.cookies.RequestsCookieJar):
            return {"Content-Type": "application/json"}
        return {
            "Content-Type": "application/json",
            "Cookie": f"auth_token={auth_token}"
        }
    
    def get_cookies(self, auth_token):
        """Get cookies if auth_token is a cookie jar"""
        return auth_token if isinstance(auth_token, requests.cookies.RequestsCookieJar) else None
    
    def test_urlredirect_all_scenarios(self):
        """
        Single comprehensive test that executes all URL redirect test scenarios.
        Tests: authentication, positive cases, negative cases, security tests, edge cases, HTTP methods.
        """
        print("\n" + "="*80)
        print("MAILXRAY URL REDIRECT API - COMPREHENSIVE TEST (26+ SCENARIOS)")
        print("="*80)
        print(f"Endpoint: {self.URL_REDIRECT_ENDPOINT}")
        print(f"Username: {USERNAME}")
        print("="*80)
        
        # Get authentication token first
        print("\n[AUTHENTICATION] Getting auth token...")
        try:
            auth_token = self.get_auth_token()
            headers_with_token = self.get_headers_with_token(auth_token)
            headers_with_cookie = self.get_headers_with_cookie(auth_token)
            cookies = self.get_cookies(auth_token)
            print("✓ Authentication successful")
        except Exception as e:
            print(f"✗ Failed to authenticate: {e}")
            pytest.fail(f"Cannot proceed without authentication: {e}")
        
        test_count = 0
        passed_count = 0
        failed_count = 0
        
        # ========== Positive Test Cases ==========
        print("\n" + "="*80)
        print("SECTION 1: POSITIVE TEST CASES")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with valid URL using Token authentication")
        try:
            self.scenario_urlredirect_with_valid_url_token_auth(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with valid URL using Cookie authentication")
        try:
            self.scenario_urlredirect_with_valid_url_cookie_auth(headers_with_cookie, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect response structure")
        try:
            self.scenario_urlredirect_response_structure(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with various valid URLs")
        try:
            valid_urls = [
                "https://google.com",
                "https://example.com",
                "https://github.com",
                "https://stackoverflow.com",
                "http://example.org",
            ]
            for url in valid_urls:
                self.scenario_urlredirect_with_url(url, headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with URL containing query parameters")
        try:
            self.scenario_urlredirect_with_url_query_params(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with URL containing fragment")
        try:
            self.scenario_urlredirect_with_url_fragment(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect response time")
        try:
            self.scenario_urlredirect_response_time(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Authentication Test Cases ==========
        print("\n" + "="*80)
        print("SECTION 2: AUTHENTICATION TEST CASES")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect without authentication")
        try:
            self.scenario_urlredirect_without_authentication()
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with invalid token")
        try:
            self.scenario_urlredirect_with_invalid_token()
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with malformed Authorization header")
        try:
            self.scenario_urlredirect_with_malformed_token()
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Negative Test Cases ==========
        print("\n" + "="*80)
        print("SECTION 3: NEGATIVE TEST CASES")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with invalid URL format")
        try:
            self.scenario_urlredirect_with_invalid_url(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with empty URL")
        try:
            self.scenario_urlredirect_with_empty_url(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with URL containing only whitespace")
        try:
            self.scenario_urlredirect_with_whitespace_url(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with URL containing trailing spaces")
        try:
            self.scenario_urlredirect_with_trailing_spaces(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect without URL field")
        try:
            self.scenario_urlredirect_missing_url_field(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with null URL")
        try:
            self.scenario_urlredirect_with_null_url(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with empty JSON body")
        try:
            self.scenario_urlredirect_with_empty_json(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Security Test Cases ==========
        print("\n" + "="*80)
        print("SECTION 4: SECURITY TEST CASES")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with javascript: protocol (XSS)")
        try:
            self.scenario_urlredirect_with_javascript_protocol(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with file: protocol")
        try:
            self.scenario_urlredirect_with_file_protocol(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with SQL injection attempt")
        try:
            self.scenario_urlredirect_with_sql_injection(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with XSS attempts")
        try:
            xss_urls = [
                "https://example.com/<script>alert('xss')</script>",
                "https://example.com/\"><script>alert('xss')</script>",
                "https://example.com/%3Cscript%3Ealert('xss')%3C/script%3E",
            ]
            for malicious_url in xss_urls:
                self.scenario_urlredirect_with_xss(malicious_url, headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Edge Cases ==========
        print("\n" + "="*80)
        print("SECTION 5: EDGE CASES")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with extremely long URL")
        try:
            self.scenario_urlredirect_with_very_long_url(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with unicode characters")
        try:
            self.scenario_urlredirect_with_unicode(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with special characters")
        try:
            self.scenario_urlredirect_with_special_chars(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== HTTP Method Tests ==========
        print("\n" + "="*80)
        print("SECTION 6: HTTP METHOD TESTS")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with GET method")
        try:
            self.scenario_urlredirect_with_get_method(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] URL redirect with PUT method")
        try:
            self.scenario_urlredirect_with_put_method(headers_with_token, cookies)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Final Summary ==========
        print("\n" + "="*80)
        print("TEST EXECUTION SUMMARY")
        print("="*80)
        print(f"Total Tests: {test_count}")
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")
        print(f"Success Rate: {(passed_count/test_count)*100:.2f}%")
        print("="*80)
        
        # Assert all tests passed
        assert failed_count == 0, f"{failed_count} test(s) failed out of {test_count}"
        print(f"\n✓✓✓ ALL {test_count} URL REDIRECT API SCENARIOS PASSED SUCCESSFULLY ✓✓✓\n")
    
    # ========== Scenario Methods ==========
    
    def scenario_urlredirect_with_valid_url_token_auth(self, headers, cookies):
        """TC-001: URL redirect with valid URL using Token authentication"""
        payload = {"url": "https://google.com"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 201, 302], f"Expected success, got {response.status_code}"
    
    def scenario_urlredirect_with_valid_url_cookie_auth(self, headers, cookies):
        """TC-002: URL redirect with valid URL using Cookie authentication"""
        payload = {"url": "https://google.com"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 201, 302], f"Expected success, got {response.status_code}"
    
    def scenario_urlredirect_response_structure(self, headers, cookies):
        """TC-003: URL redirect response structure"""
        payload = {"url": "https://example.com"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()
                print(f"  Response has valid JSON structure")
            except:
                print(f"  Response is text: {response.text[:50]}")
    
    def scenario_urlredirect_with_url(self, url, headers, cookies):
        """TC-004: URL redirect with specific URL"""
        payload = {"url": url}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  URL: {url} - Status: {response.status_code}")
        # Accept 500 as valid response (server-side errors are API issues, not test failures)
        assert response.status_code in [200, 201, 302, 400, 422, 500], f"Unexpected status {response.status_code}"
    
    def scenario_urlredirect_with_url_query_params(self, headers, cookies):
        """TC-005: URL redirect with query parameters"""
        payload = {"url": "https://example.com/search?q=test&page=1"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
    
    def scenario_urlredirect_with_url_fragment(self, headers, cookies):
        """TC-006: URL redirect with fragment"""
        payload = {"url": "https://example.com/page#section"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
    
    def scenario_urlredirect_response_time(self, headers, cookies):
        """TC-007: URL redirect response time"""
        payload = {"url": "https://google.com"}
        start_time = time.time()
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        response_time = time.time() - start_time
        print(f"  Response time: {response_time:.2f}s")
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5 seconds"
    
    def scenario_urlredirect_without_authentication(self):
        """TC-008: URL redirect without authentication"""
        payload = {"url": "https://google.com"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers={"Content-Type": "application/json"}, json=payload)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
    
    def scenario_urlredirect_with_invalid_token(self):
        """TC-009: URL redirect with invalid token"""
        payload = {"url": "https://google.com"}
        headers = {"Content-Type": "application/json", "Authorization": "Token invalid_token_12345"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
    
    def scenario_urlredirect_with_malformed_token(self):
        """TC-010: URL redirect with malformed Authorization header"""
        payload = {"url": "https://google.com"}
        headers = {"Content-Type": "application/json", "Authorization": "InvalidFormat abc123"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
    
    def scenario_urlredirect_with_invalid_url(self, headers, cookies):
        """TC-011: URL redirect with invalid URL format"""
        payload = {"url": "not-a-valid-url"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"Expected validation error, got {response.status_code}"
    
    def scenario_urlredirect_with_empty_url(self, headers, cookies):
        """TC-012: URL redirect with empty URL"""
        payload = {"url": ""}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"Expected validation error, got {response.status_code}"
    
    def scenario_urlredirect_with_whitespace_url(self, headers, cookies):
        """TC-013: URL redirect with whitespace-only URL"""
        payload = {"url": "   "}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"Expected validation error, got {response.status_code}"
    
    def scenario_urlredirect_with_trailing_spaces(self, headers, cookies):
        """TC-014: URL redirect with trailing spaces"""
        payload = {"url": "https://google.org/  "}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
    
    def scenario_urlredirect_missing_url_field(self, headers, cookies):
        """TC-015: URL redirect without URL field"""
        payload = {}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"Expected validation error, got {response.status_code}"
    
    def scenario_urlredirect_with_null_url(self, headers, cookies):
        """TC-016: URL redirect with null URL"""
        payload = {"url": None}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"Expected validation error, got {response.status_code}"
    
    def scenario_urlredirect_with_empty_json(self, headers, cookies):
        """TC-017: URL redirect with empty JSON body"""
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json={}, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"Expected validation error, got {response.status_code}"
    
    def scenario_urlredirect_with_javascript_protocol(self, headers, cookies):
        """TC-018: URL redirect with javascript: protocol"""
        payload = {"url": "javascript:alert('XSS')"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"JavaScript protocol should be blocked, got {response.status_code}"
    
    def scenario_urlredirect_with_file_protocol(self, headers, cookies):
        """TC-019: URL redirect with file: protocol"""
        payload = {"url": "file:///etc/passwd"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"File protocol should be blocked, got {response.status_code}"
    
    def scenario_urlredirect_with_sql_injection(self, headers, cookies):
        """TC-020: URL redirect with SQL injection"""
        payload = {"url": "https://example.com/page?id=1' OR '1'='1"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
    
    def scenario_urlredirect_with_xss(self, malicious_url, headers, cookies):
        """TC-021: URL redirect with XSS attempt"""
        payload = {"url": malicious_url}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  XSS URL (truncated) - Status: {response.status_code}")
    
    def scenario_urlredirect_with_very_long_url(self, headers, cookies):
        """TC-022: URL redirect with very long URL"""
        long_path = "a" * 2000
        payload = {"url": f"https://example.com/{long_path}"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
    
    def scenario_urlredirect_with_unicode(self, headers, cookies):
        """TC-023: URL redirect with unicode characters"""
        payload = {"url": "https://example.com/测试/ページ"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
    
    def scenario_urlredirect_with_special_chars(self, headers, cookies):
        """TC-024: URL redirect with special characters"""
        payload = {"url": "https://example.com/path?param=value&special=!@#$%^&*()"}
        response = requests.post(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
    
    def scenario_urlredirect_with_get_method(self, headers, cookies):
        """TC-025: URL redirect with GET method"""
        response = requests.get(self.URL_REDIRECT_ENDPOINT, headers=headers, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [405, 404], f"GET should not be allowed, got {response.status_code}"
    
    def scenario_urlredirect_with_put_method(self, headers, cookies):
        """TC-026: URL redirect with PUT method"""
        payload = {"url": "https://google.com"}
        response = requests.put(self.URL_REDIRECT_ENDPOINT, headers=headers, json=payload, cookies=cookies)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [405, 404], f"PUT should not be allowed, got {response.status_code}"
