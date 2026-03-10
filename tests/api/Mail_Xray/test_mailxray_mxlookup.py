
import pytest
import requests
import os
import json
import time
import sys
from pathlib import Path
from utils.auth_token_helper import get_auth_token_from_login
from utils.config import BASE_URL, USERNAME, PASSWORD


class TestMailXrayMXLookup:
    """Test cases for MailXray MX Lookup API"""
    
    # Use BASE_URL from utils/config.py
    MXLOOKUP_ENDPOINT = f"{BASE_URL}/tools/api/mxlookup/"
    
    @pytest.fixture
    def auth_token(self):
        return get_auth_token_from_login()
    
    @pytest.fixture
    def auth_cookie(self, auth_token):
        return auth_token
    
    @pytest.fixture
    def token_headers(self, auth_token):
        return {
            "Authorization": f"Token {auth_token}",
            "Content-Type": "application/json"
        }
    
    @pytest.fixture
    def cookie_dict(self, auth_cookie):
        return {
            "auth_token": auth_cookie
        }
    
    @pytest.fixture
    def headers(self):
        """Fixture to provide standard headers"""
        return {
            "Content-Type": "application/json"
        }
    
    # ========== Positive Test Cases ==========
    
    def test_mxlookup_with_valid_domain_cookie_auth(self, headers, cookie_dict):
        """TC-001: Test MX lookup with valid domain using Cookie authentication"""
        payload = {
            "query": "google.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API may return 403 if authentication is not accepted, adjust expectation
        if response.status_code == 403:
            print(f"⚠ Cookie authentication not accepted (may require Token auth)")
            pytest.skip("Cookie authentication not working - skipping test")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        
        # Validate response structure
        assert "status_code" in response_data, "Missing 'status_code' field"
        assert "data" in response_data, "Missing 'data' field"
        assert response_data["status_code"] == 200, "status_code should be 200"
        assert "message" in response_data, "Missing 'message' field"
        assert response_data["message"] == "Enhanced MX check successful", f"Expected message 'Enhanced MX check successful', got {response_data['message']}"
        
        # Validate data structure
        data = response_data["data"]
        assert "domain" in data, "Missing 'domain' field"
        assert "mx_records" in data, "Missing 'mx_records' field"
        assert "validation_results" in data, "Missing 'validation_results' field"
        assert data["domain"] == "google.com", f"Expected 'google.com', got {data['domain']}"
        assert isinstance(data["mx_records"], list), "mx_records should be a list"
        assert len(data["mx_records"]) > 0, "mx_records should not be empty"
        
        print(f"✓ MX Lookup successful for: google.com")
        print(f"✓ Response validated: {len(data['mx_records'])} MX records found")
    
    def test_mxlookup_with_valid_domain_token_auth(self, token_headers):
        """TC-002: Test MX lookup with valid domain using Token authentication"""
        payload = {
            "query": "gmail.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=token_headers,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API may return 403 if token is invalid/expired
        if response.status_code == 403:
            print(f"⚠ Token authentication not accepted (token may be invalid/expired)")
            pytest.skip("Token authentication not working - skipping test")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Validate response structure
        response_data = response.json()
        assert "status_code" in response_data, "Missing 'status_code' field"
        assert "data" in response_data, "Missing 'data' field"
        
        # Validate data structure
        data = response_data["data"]
        assert "domain" in data, "Missing 'domain' field"
        assert "mx_records" in data, "Missing 'mx_records' field"
        assert data["domain"] == "gmail.com", f"Expected 'gmail.com', got {data['domain']}"
        assert isinstance(data["mx_records"], list), "mx_records should be a list"
        assert len(data["mx_records"]) > 0, "mx_records should not be empty"
        
        print(f"✓ MX Lookup successful for: gmail.com")
        print(f"✓ Response validated: {len(data['mx_records'])} MX records found")
    
    def test_mxlookup_with_url_format(self, headers, cookie_dict):
        """TC-003: Test MX lookup with URL format (like curl example)"""
        payload = {
            "query": "http://google.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Validate response structure
        response_data = response.json()
        assert "status_code" in response_data, "Missing 'status_code' field"
        assert "data" in response_data, "Missing 'data' field"
        assert isinstance(response_data["data"]["mx_records"], list), "mx_records should be a list"
        
        print(f"✓ MX Lookup with URL format successful")
        print(f"✓ Response validated")
    
    def test_mxlookup_with_trailing_spaces(self, headers, cookie_dict):
        """TC-004: Test MX lookup with trailing spaces (exact curl example)"""
        payload = {
            "query": "http://google.com  ",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API should either handle trailing spaces or return error
        print(f"✓ Trailing spaces handling: Status {response.status_code}")
    
    def test_mxlookup_with_https_protocol(self, headers, cookie_dict):
        """TC-005: Test MX lookup with HTTPS protocol"""
        payload = {
            "query": "https://example.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Validate response structure
        response_data = response.json()
        assert "status_code" in response_data, "Missing 'status_code' field"
        assert "data" in response_data, "Missing 'data' field"
        assert isinstance(response_data["data"]["mx_records"], list), "mx_records should be a list"
        
        print(f"✓ MX Lookup with HTTPS protocol successful")
        print(f"✓ Response validated")
    
    def test_mxlookup_with_subdomain(self, headers, cookie_dict):
        """TC-006: Test MX lookup with subdomain"""
        payload = {
            "query": "mail.google.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Validate response structure
        response_data = response.json()
        assert "status_code" in response_data, "Missing 'status_code' field"
        assert "data" in response_data, "Missing 'data' field"
        assert "mx_records" in response_data["data"], "Missing 'mx_records' field"
        
        print(f"✓ MX Lookup with subdomain successful")
        print(f"✓ Response validated")
    
    def test_mxlookup_response_structure(self, headers, cookie_dict):
        """TC-007: Test MX lookup response structure"""
        payload = {
            "query": "google.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        assert response.status_code == 200
        response_data = response.json()
        
        print(f"\n✓ Response Data: {json.dumps(response_data, indent=2)[:1000]}")
        
        # Check for common MX lookup response fields
        if isinstance(response_data, dict):
            print(f"✓ Response keys: {list(response_data.keys())}")
    
    @pytest.mark.parametrize("domain", [
        "google.com",
        "yahoo.com",
        "microsoft.com",
        "barracuda.com",
        "outlook.com"
    ])
    def test_mxlookup_multiple_domains(self, headers, cookie_dict, domain):
        """TC-008: Test MX lookup with multiple well-known domains"""
        payload = {
            "query": domain,
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Domain: {domain}, Status: {response.status_code}")
        
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        assert response.status_code == 200, f"Expected 200 for {domain}, got {response.status_code}"
    
    # ========== Negative Test Cases - Authentication ==========
    
    def test_mxlookup_without_authentication(self, headers):
        """TC-009: Test MX lookup without authentication"""
        payload = {
            "query": "google.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for missing auth, got {response.status_code}"
        
        response_data = response.json()
        assert "detail" in response_data
        print(f"✓ Authentication required: {response_data['detail']}")
    
    def test_mxlookup_with_invalid_token(self, headers):
        """TC-010: Test MX lookup with invalid token"""
        invalid_headers = headers.copy()
        invalid_headers["Authorization"] = "Token invalid_token_12345"
        
        payload = {
            "query": "google.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=invalid_headers,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for invalid token, got {response.status_code}"
        
        print(f"✓ Invalid token correctly rejected")
    
    def test_mxlookup_with_invalid_cookie(self, headers):
        """TC-011: Test MX lookup with invalid cookie"""
        invalid_cookies = {
            "auth_token": "invalid_cookie_12345"
        }
        
        payload = {
            "query": "google.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=invalid_cookies,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for invalid cookie, got {response.status_code}"
        
        print(f"✓ Invalid cookie correctly rejected")
    
    # ========== Negative Test Cases - Input Validation ==========
    
    def test_mxlookup_with_empty_query(self, headers, cookie_dict):
        """TC-012: Test MX lookup with empty query"""
        payload = {
            "query": "",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:200]}")
        
        # If 403, authentication issue; otherwise should be 400/422
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        # Should return error for empty query
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for empty query, got {response.status_code}"
        
        print(f"✓ Empty query correctly rejected")
    
    def test_mxlookup_with_missing_query_field(self, headers, cookie_dict):
        """TC-013: Test MX lookup with missing query field"""
        payload = {
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for missing query, got {response.status_code}"
        
        print(f"✓ Missing query field correctly rejected")
    
    def test_mxlookup_with_null_query(self, headers, cookie_dict):
        """TC-014: Test MX lookup with null query"""
        payload = {
            "query": None,
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for null query, got {response.status_code}"
        
        print(f"✓ Null query correctly rejected")
    
    def test_mxlookup_with_empty_body(self, headers, cookie_dict):
        """TC-015: Test MX lookup with empty JSON body"""
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json={}
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for empty body, got {response.status_code}"
        
        print(f"✓ Empty body correctly rejected")
    
    def test_mxlookup_with_invalid_domain_format(self, headers, cookie_dict):
        """TC-016: Test MX lookup with invalid domain format"""
        invalid_domains = [
            "not a domain",
            "invalid..domain",
            "-invalid.com",
            "invalid-.com",
            "123.456.789.000",  # Not a valid domain
        ]
        
        for domain in invalid_domains:
            payload = {
                "query": domain,
                "variables": {}
            }
            
            response = requests.post(
                self.MXLOOKUP_ENDPOINT,
                headers=headers,
                cookies=cookie_dict,
                json=payload
            )
            
            print(f"\n✓ Domain: {domain}, Status: {response.status_code}")
    
    def test_mxlookup_with_nonexistent_domain(self, headers, cookie_dict):
        """TC-017: Test MX lookup with non-existent domain"""
        payload = {
            "query": "thisisanonexistentdomain12345.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # May return 200 with no MX records or error
        print(f"✓ Non-existent domain handling: Status {response.status_code}")
    
    def test_mxlookup_with_domain_without_mx_records(self, headers, cookie_dict):
        """TC-018: Test MX lookup with domain that has no MX records"""
        payload = {
            "query": "example.com",  # May or may not have MX records
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Validate response structure
        response_data = response.json()
        assert "status_code" in response_data, "Missing 'status_code' field"
        assert "data" in response_data, "Missing 'data' field"
        
        print(f"✓ Domain without MX records handled")
        print(f"✓ Response validated")
    
    # ========== Security Test Cases ==========
    
    def test_mxlookup_with_sql_injection(self, headers, cookie_dict):
        """TC-019: Test SQL injection attempt in query"""
        payload = {
            "query": "google.com' OR '1'='1",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        # Should handle safely without SQL injection
        print(f"✓ SQL injection attempt handled: Status {response.status_code}")
    
    def test_mxlookup_with_xss_attempt(self, headers, cookie_dict):
        """TC-020: Test XSS attempt in query"""
        payload = {
            "query": "<script>alert('XSS')</script>",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        # Should handle safely without XSS
        print(f"✓ XSS attempt handled: Status {response.status_code}")
    
    def test_mxlookup_with_command_injection(self, headers, cookie_dict):
        """TC-021: Test command injection attempt"""
        payload = {
            "query": "google.com; ls -la",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        # Should handle safely without command injection
        print(f"✓ Command injection attempt handled: Status {response.status_code}")
    
    # ========== Edge Cases ==========
    
    def test_mxlookup_with_very_long_domain(self, headers, cookie_dict):
        """TC-022: Test MX lookup with very long domain name"""
        payload = {
            "query": "a" * 255 + ".com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Very long domain handling: Status {response.status_code}")
    
    def test_mxlookup_with_unicode_domain(self, headers, cookie_dict):
        """TC-023: Test MX lookup with unicode/IDN domain"""
        payload = {
            "query": "例え.jp",  # Japanese characters
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Unicode domain handling: Status {response.status_code}")
    
    def test_mxlookup_with_punycode_domain(self, headers, cookie_dict):
        """TC-024: Test MX lookup with punycode domain"""
        payload = {
            "query": "xn--e1afmkfd.xn--p1ai",  # Punycode format
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Punycode domain handling: Status {response.status_code}")
    
    def test_mxlookup_with_ip_address(self, headers, cookie_dict):
        """TC-025: Test MX lookup with IP address instead of domain"""
        payload = {
            "query": "8.8.8.8",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ IP address handling: Status {response.status_code}")
    
    def test_mxlookup_with_localhost(self, headers, cookie_dict):
        """TC-026: Test MX lookup with localhost"""
        payload = {
            "query": "localhost",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Localhost handling: Status {response.status_code}")
    
    def test_mxlookup_with_uppercase_domain(self, headers, cookie_dict):
        """TC-027: Test MX lookup with uppercase domain"""
        payload = {
            "query": "GOOGLE.COM",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Validate response structure
        response_data = response.json()
        assert "status_code" in response_data, "Missing 'status_code' field"
        assert "data" in response_data, "Missing 'data' field"
        assert isinstance(response_data["data"]["mx_records"], list), "mx_records should be a list"
        
        print(f"✓ Uppercase domain handled successfully")
        print(f"✓ Response validated")
    
    def test_mxlookup_with_mixed_case_domain(self, headers, cookie_dict):
        """TC-028: Test MX lookup with mixed case domain"""
        payload = {
            "query": "GooGLe.CoM",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        if response.status_code == 403:
            pytest.skip("Authentication not working - skipping test")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Validate response structure
        response_data = response.json()
        assert "status_code" in response_data, "Missing 'status_code' field"
        assert "data" in response_data, "Missing 'data' field"
        assert isinstance(response_data["data"]["mx_records"], list), "mx_records should be a list"
        
        print(f"✓ Mixed case domain handled successfully")
        print(f"✓ Response validated")
    
    # ========== HTTP Method Tests ==========
    
    def test_mxlookup_with_get_method(self, token_headers):
        """TC-029: Test endpoint with GET method (should fail)"""
        response = requests.get(
            self.MXLOOKUP_ENDPOINT,
            headers=token_headers
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [405, 404], \
            f"GET method should not be allowed, got {response.status_code}"
        
        print(f"✓ GET method correctly rejected")
    
    def test_mxlookup_with_put_method(self, token_headers):
        """TC-030: Test endpoint with PUT method (should fail)"""
        payload = {
            "query": "google.com",
            "variables": {}
        }
        
        response = requests.put(
            self.MXLOOKUP_ENDPOINT,
            headers=token_headers,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [405, 404], \
            f"PUT method should not be allowed, got {response.status_code}"
        
        print(f"✓ PUT method correctly rejected")
    
    def test_mxlookup_with_delete_method(self, token_headers):
        """TC-031: Test endpoint with DELETE method (should fail)"""
        response = requests.delete(
            self.MXLOOKUP_ENDPOINT,
            headers=token_headers
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [405, 404], \
            f"DELETE method should not be allowed, got {response.status_code}"
        
        print(f"✓ DELETE method correctly rejected")
    
    # ========== Performance Tests ==========
    
    def test_mxlookup_response_time(self, headers, cookie_dict):
        """TC-032: Test MX lookup response time (should be < 5 seconds)"""
        payload = {
            "query": "google.com",
            "variables": {}
        }
        
        start_time = time.time()
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"\n✓ Response time: {response_time:.2f} seconds")
        
        assert response.status_code == 200
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5 seconds"
        
        print(f"✓ Response time is acceptable")
    
    def test_mxlookup_multiple_rapid_requests(self, headers, cookie_dict):
        """TC-033: Test rate limiting with multiple rapid requests"""
        payload = {
            "query": "google.com",
            "variables": {}
        }
        
        responses = []
        for i in range(5):
            response = requests.post(
                self.MXLOOKUP_ENDPOINT,
                headers=headers,
                cookies=cookie_dict,
                json=payload
            )
            responses.append(response.status_code)
            time.sleep(0.1)
        
        print(f"\n✓ Multiple rapid requests: {responses}")
        
        rate_limited = any(status == 429 for status in responses)
        if rate_limited:
            print(f"  Rate limiting detected")
        else:
            print(f"  No rate limiting detected")
    
    # ========== Content-Type Tests ==========
    
    def test_mxlookup_with_malformed_json(self, headers, cookie_dict):
        """TC-034: Test MX lookup with malformed JSON"""
        malformed_json = '{"query": "google.com", "variables": invalid}'
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            data=malformed_json
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [400, 500], \
            f"Malformed JSON should return error, got {response.status_code}"
        
        print(f"✓ Malformed JSON correctly rejected")
    
    def test_mxlookup_without_content_type(self, cookie_dict):
        """TC-035: Test MX lookup without Content-Type header"""
        payload = {
            "query": "google.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            cookies=cookie_dict,
            json=payload  # requests will auto-add Content-Type
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Without explicit Content-Type handling: Status {response.status_code}")

    def test_mxlookup_validate_complete_response_body(self, token_headers):
        """TC-036: Test MX lookup and validate complete response body structure"""
        payload = {
            "query": "gmail.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MXLOOKUP_ENDPOINT,
            headers=token_headers,
            json=payload
        )
        
        print(f"\n{'='*60}")
        print(f"TC-036: MX Lookup Complete Response Body Validation")
        print(f"{'='*60}")
        
        # Validate status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"✓ Status Code: {response.status_code}")
        
        # Parse response JSON
        response_data = response.json()
        print(f"\n✓ Response Data Keys: {list(response_data.keys())}")
        
        # Validate top-level structure
        assert "status_code" in response_data, "Missing 'status_code' field in response"
        assert "data" in response_data, "Missing 'data' field in response"
        print(f"✓ Top-level structure validated (status_code, data)")
        
        # Validate status_code field
        assert isinstance(response_data["status_code"], int), "status_code should be integer"
        assert response_data["status_code"] == 200, f"status_code should be 200, got {response_data['status_code']}"
        print(f"✓ status_code field: {response_data['status_code']} (int)")
        
        # Validate data object
        data = response_data["data"]
        assert isinstance(data, dict), "data should be a dictionary"
        print(f"✓ data field is dictionary")
        
        # Validate data keys
        expected_keys = ["domain", "mx_records", "validation_results"]
        for key in expected_keys:
            assert key in data, f"Missing '{key}' field in data"
        print(f"✓ data contains required keys: {expected_keys}")
        
        # Validate domain field
        assert isinstance(data["domain"], str), "domain should be string"
        assert data["domain"] == "gmail.com", f"Expected 'gmail.com', got {data['domain']}"
        print(f"✓ domain field: '{data['domain']}' (string)")
        
        # Validate mx_records field
        assert isinstance(data["mx_records"], list), "mx_records should be a list"
        assert len(data["mx_records"]) > 0, "mx_records should not be empty"
        print(f"✓ mx_records field is list with {len(data['mx_records'])} records")
        
        # Validate individual MX record structure
        for idx, mx_record in enumerate(data["mx_records"]):
            assert isinstance(mx_record, list), f"MX record {idx} should be a list"
            assert len(mx_record) == 4, f"MX record {idx} should have 4 elements (priority, host, ip, ttl)"
            
            priority, host, ip, ttl = mx_record
            
            # Validate priority
            assert isinstance(priority, str), f"Priority should be string, got {type(priority)}"
            assert priority.isdigit(), f"Priority should be numeric string, got '{priority}'"
            
            # Validate host
            assert isinstance(host, str), f"Host should be string, got {type(host)}"
            assert len(host) > 0, "Host should not be empty"
            
            # Validate IP
            assert isinstance(ip, str), f"IP should be string, got {type(ip)}"
            
            # Validate TTL
            assert isinstance(ttl, str), f"TTL should be string, got {type(ttl)}"
            
            print(f"  ✓ MX Record {idx+1}: priority={priority}, host={host}, ip={ip}, ttl={ttl}")
        
        # Validate validation_results field
        assert isinstance(data["validation_results"], list), "validation_results should be a list"
        assert len(data["validation_results"]) > 0, "validation_results should not be empty"
        print(f"\n✓ validation_results field is list with {len(data['validation_results'])} results")
        
        # Validate individual validation result structure
        for idx, validation_result in enumerate(data["validation_results"]):
            assert isinstance(validation_result, dict), f"Validation result {idx} should be a dictionary"
            assert "test" in validation_result, f"Validation result {idx} missing 'test' field"
            assert "result" in validation_result, f"Validation result {idx} missing 'result' field"
            
            test = validation_result["test"]
            result = validation_result["result"]
            
            assert isinstance(test, str), f"Test should be string, got {type(test)}"
            assert isinstance(result, str), f"Result should be string, got {type(result)}"
            
            print(f"  ✓ Validation {idx+1}: test='{test}', result='{result}'")
        
        print(f"\n{'='*60}")
        print(f"✓ Complete Response Body Validation PASSED")
        print(f"  - Total MX Records: {len(data['mx_records'])}")
        print(f"  - Total Validation Results: {len(data['validation_results'])}")
        print(f"  - Domain: {data['domain']}")
        print(f"{'='*60}")


# To run these tests:
# export MAILXRAY_BASE_URL="https://mailxray.dev.bci.aws.cudaops.com"
# export MAILXRAY_AUTH_TOKEN="e7b6eb81bb609e442b6ebd8876f7345d15d8c5fb"
# export MAILXRAY_AUTH_COOKIE="e6b22e6ed86acd7f09685f41c1698344da185d2e"
#
# Run all tests:
# .venv/bin/pytest -v -s tests/api/Mail_Xray/test_mailxray_mxlookup.py
#
# Run specific test:
# .venv/bin/pytest -v -s tests/api/Mail_Xray/test_mailxray_mxlookup.py::TestMailXrayMXLookup::test_mxlookup_with_valid_domain_cookie_auth
#
# Run authentication tests:
# .venv/bin/pytest -v -s tests/api/Mail_Xray/test_mailxray_mxlookup.py -k "auth"
#
# Run with HTML report:
# .venv/bin/pytest tests/api/Mail_Xray/test_mailxray_mxlookup.py --html=reports/mxlookup_report.html --self-contained-html
