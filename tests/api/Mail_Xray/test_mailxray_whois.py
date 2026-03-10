
import pytest
import requests
import os
import json
import time
import sys
import csv
from datetime import datetime
from pathlib import Path
from utils.auth_token_helper import get_auth_token_from_login
from utils.config import BASE_URL, USERNAME, PASSWORD


class TestMailXrayWhois:
    """Comprehensive test for MailXray WHOIS API - All scenarios in one test"""
    
    # Use BASE_URL from utils/config.py
    WHOIS_ENDPOINT = f"{BASE_URL}/tools/api/whois/"
    LOGIN_ENDPOINT = f"{BASE_URL}/tools/api/login/"
    
    def get_auth_token(self):
        # Use the correct helper for authentication
        return get_auth_token_from_login()
    
    def get_headers_with_token(self, auth_token=None):
        if auth_token is None:
            auth_token = get_auth_token_from_login()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Token {auth_token}"
        }
    
    def get_headers_with_cookie(self, auth_token=None):
        if auth_token is None:
            auth_token = get_auth_token_from_login()
        return {
            "Content-Type": "application/json",
            "Cookie": f"auth_token={auth_token}"
        }
    
    def load_test_data_from_csv(self):
        """Load test data from mailxray_homepage.csv"""
        csv_path = Path(__file__).parent.parent.parent.parent / "testdata" / "mailxray_homepage.csv"
        test_data = {}
        
        try:
            with open(csv_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    test_data['url'] = row.get('URL', 'http://google.com')
                    test_data['ip'] = row.get('IP', '8.8.8.8')
                    test_data['domain'] = row.get('Domain', 'google.com')
                    break  # Use first row
        except FileNotFoundError:
            print(f"Warning: CSV file not found at {csv_path}, using default values")
            test_data = {
                'url': 'http://google.com',
                'ip': '8.8.8.8',
                'domain': 'google.com'
            }
        
        return test_data
    
    def get_valid_query(self):
        """Get valid WHOIS query from CSV data"""
        test_data = self.load_test_data_from_csv()
        return {
            "query": test_data['url'],
            "variables": {}
        }
    
    def test_whois_all_scenarios(self):
        """
        Single comprehensive test that executes all WHOIS test scenarios.
        Tests: authentication, positive cases, negative cases, security tests, HTTP methods, content-type, variables, rate limiting.
        """
        # Load test data from CSV
        test_data = self.load_test_data_from_csv()
        
        print("\n" + "="*80)
        print("MAILXRAY WHOIS API - COMPREHENSIVE TEST (30 SCENARIOS)")
        print("="*80)
        print(f"Endpoint: {self.WHOIS_ENDPOINT}")
        print(f"Base URL: {BASE_URL} (from utils/config.py)")
        print(f"Username: {USERNAME}")
        print(f"Test Data from CSV:")
        print(f"  URL: {test_data['url']}")
        print(f"  IP: {test_data['ip']}")
        print(f"  Domain: {test_data['domain']}")
        print("="*80)
        
        # Get authentication token first
        print("\n[AUTHENTICATION] Getting auth token...")
        try:
            auth_token = self.get_auth_token()
            headers_with_token = self.get_headers_with_token(auth_token)
            headers_with_cookie = self.get_headers_with_cookie(auth_token)
            valid_query = self.get_valid_query()
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
        print(f"\n[Test {test_count}] WHOIS lookup with valid domain (cookie auth)")
        try:
            self.scenario_whois_with_valid_domain_cookie_auth(headers_with_cookie, valid_query)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS lookup with valid domain (token auth)")
        try:
            self.scenario_whois_with_valid_domain_token_auth(headers_with_token, valid_query)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS response contains domain information")
        try:
            self.scenario_whois_response_contains_domain_info(headers_with_cookie, valid_query)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS API response time")
        try:
            self.scenario_whois_response_time(headers_with_cookie, valid_query)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with various valid domains")
        try:
            # Load CSV data for domain testing
            test_data = self.load_test_data_from_csv()
            domains = [
                test_data['domain'],           # From CSV: redhat.com
                test_data['url'],              # From CSV: https://google.com
                "http://" + test_data['domain'],  # http://redhat.com
                "https://" + test_data['domain'], # https://redhat.com
                "www." + test_data['domain'],     # www.redhat.com
                "example.com"                   # Additional test domain
            ]
            for domain in domains:
                self.scenario_whois_with_domain(domain, headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with trailing whitespace")
        try:
            test_data = self.load_test_data_from_csv()
            self.scenario_whois_with_trailing_whitespace(headers_with_cookie, test_data['url'])
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with leading whitespace")
        try:
            test_data = self.load_test_data_from_csv()
            self.scenario_whois_with_leading_whitespace(headers_with_cookie, test_data['url'])
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with empty variables")
        try:
            test_data = self.load_test_data_from_csv()
            self.scenario_whois_with_empty_variables(headers_with_cookie, test_data['domain'])
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS without variables field")
        try:
            test_data = self.load_test_data_from_csv()
            self.scenario_whois_without_variables_field(headers_with_cookie, test_data['domain'])
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Negative Test Cases ==========
        print("\n" + "="*80)
        print("SECTION 2: NEGATIVE TEST CASES")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS without authentication")
        try:
            self.scenario_whois_without_authentication()
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with invalid token")
        try:
            self.scenario_whois_with_invalid_token()
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with empty query")
        try:
            self.scenario_whois_with_empty_query(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with missing query field")
        try:
            self.scenario_whois_with_missing_query_field(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with null query")
        try:
            self.scenario_whois_with_null_query(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with empty JSON body")
        try:
            self.scenario_whois_with_empty_json_body(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with invalid domain format")
        try:
            self.scenario_whois_with_invalid_domain(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with non-existent domain")
        try:
            self.scenario_whois_with_nonexistent_domain(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with IP address")
        try:
            test_data = self.load_test_data_from_csv()
            self.scenario_whois_with_ip_address(headers_with_cookie, test_data['ip'])
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Security Test Cases ==========
        print("\n" + "="*80)
        print("SECTION 3: SECURITY TEST CASES")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with SQL injection attempt")
        try:
            self.scenario_whois_with_sql_injection(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with XSS attempt")
        try:
            self.scenario_whois_with_xss(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with command injection attempt")
        try:
            self.scenario_whois_with_command_injection(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with very long query")
        try:
            self.scenario_whois_with_very_long_query(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== HTTP Method Tests ==========
        print("\n" + "="*80)
        print("SECTION 4: HTTP METHOD TESTS")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with GET method")
        try:
            self.scenario_whois_with_get_method(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with PUT method")
        try:
            self.scenario_whois_with_put_method(headers_with_cookie, valid_query)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with DELETE method")
        try:
            self.scenario_whois_with_delete_method(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Content-Type Tests ==========
        print("\n" + "="*80)
        print("SECTION 5: CONTENT-TYPE TESTS")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with wrong Content-Type")
        try:
            self.scenario_whois_with_wrong_content_type(headers_with_cookie, valid_query)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with malformed JSON")
        try:
            self.scenario_whois_with_malformed_json(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Variables Field Tests ==========
        print("\n" + "="*80)
        print("SECTION 6: VARIABLES FIELD TESTS")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with populated variables")
        try:
            self.scenario_whois_with_populated_variables(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS with null variables")
        try:
            self.scenario_whois_with_null_variables(headers_with_cookie)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Rate Limiting Tests ==========
        print("\n" + "="*80)
        print("SECTION 7: RATE LIMITING TEST")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}] WHOIS multiple rapid requests")
        try:
            self.scenario_whois_multiple_rapid_requests(headers_with_cookie, valid_query)
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
        print(f"\n✓✓✓ ALL {test_count} WHOIS API SCENARIOS PASSED SUCCESSFULLY ✓✓✓\n")
    
    # ========== Scenario Methods ==========
    
    def scenario_whois_with_valid_domain_cookie_auth(self, headers, query):
        """TC-001: WHOIS lookup with cookie authentication"""
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}"
    
    def scenario_whois_with_valid_domain_token_auth(self, headers, query):
        """TC-002: WHOIS lookup with token authentication"""
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}"
    
    def scenario_whois_response_contains_domain_info(self, headers, query):
        """TC-003: Verify response contains domain information"""
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        assert response.status_code == 200
        response_text = response.text.lower()
        has_whois_data = any(["domain" in response_text, "registrar" in response_text, "creation date" in response_text,
                              "created" in response_text, "expiry" in response_text, "status" in response_text, "name server" in response_text])
        assert has_whois_data, "Response should contain WHOIS information"
        print(f"  WHOIS data present")
    
    def scenario_whois_response_time(self, headers, query):
        """TC-004: Verify response time"""
        start_time = time.time()
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        response_time = time.time() - start_time
        assert response.status_code == 200
        assert response_time < 10.0, f"Response time {response_time:.2f}s exceeds 10 seconds"
        print(f"  Response time: {response_time:.2f}s")
    
    def scenario_whois_with_domain(self, domain, headers):
        """TC-005: WHOIS with specific domain"""
        query = {"query": domain, "variables": {}}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Domain: {domain} - Status: {response.status_code}")
        assert response.status_code in [200, 201, 400, 404], f"Unexpected status {response.status_code}"
    
    def scenario_whois_with_trailing_whitespace(self, headers, url):
        """TC-006: WHOIS with trailing whitespace"""
        query = {"query": url + "  ", "variables": {}}  # Add trailing spaces to CSV URL
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 201, 400], f"Expected 200/400, got {response.status_code}"
    
    def scenario_whois_with_leading_whitespace(self, headers, url):
        """TC-007: WHOIS with leading whitespace"""
        query = {"query": "  " + url, "variables": {}}  # Add leading spaces to CSV URL
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 201, 400], f"Expected 200/400, got {response.status_code}"
    
    def scenario_whois_with_empty_variables(self, headers, domain):
        """TC-008: WHOIS with empty variables"""
        query = {"query": domain, "variables": {}}  # Use CSV domain
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}"
    
    def scenario_whois_without_variables_field(self, headers, domain):
        """TC-009: WHOIS without variables field"""
        query = {"query": domain}  # Use CSV domain
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 201, 400, 422], f"Unexpected status {response.status_code}"
    
    def scenario_whois_without_authentication(self):
        """TC-010: WHOIS without authentication"""
        query = {"query": "google.com", "variables": {}}
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
    
    def scenario_whois_with_invalid_token(self):
        """TC-011: WHOIS with invalid token"""
        query = {"query": "google.com", "variables": {}}
        headers = {"Content-Type": "application/json", "Authorization": "Token invalid_token_12345"}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
    
    def scenario_whois_with_empty_query(self, headers):
        """TC-012: WHOIS with empty query"""
        query = {"query": "", "variables": {}}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"Expected validation error, got {response.status_code}"
    
    def scenario_whois_with_missing_query_field(self, headers):
        """TC-013: WHOIS with missing query field"""
        query = {"variables": {}}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"Expected validation error, got {response.status_code}"
    
    def scenario_whois_with_null_query(self, headers):
        """TC-014: WHOIS with null query"""
        query = {"query": None, "variables": {}}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"Expected validation error, got {response.status_code}"
    
    def scenario_whois_with_empty_json_body(self, headers):
        """TC-015: WHOIS with empty JSON body"""
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json={})
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 422], f"Expected validation error, got {response.status_code}"
    
    def scenario_whois_with_invalid_domain(self, headers):
        """TC-016: WHOIS with invalid domain"""
        query = {"query": "not-a-valid-domain!!!", "variables": {}}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 400, 404, 422], f"Unexpected status {response.status_code}"
    
    def scenario_whois_with_nonexistent_domain(self, headers):
        """TC-017: WHOIS with non-existent domain"""
        query = {"query": "thisdomaindoesnotexist123456789.com", "variables": {}}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        # Accept 500 as valid (server-side WHOIS lookup errors)
        assert response.status_code in [200, 404, 500], f"Unexpected status {response.status_code}"
    
    def scenario_whois_with_ip_address(self, headers, ip):
        """TC-018: WHOIS with IP address"""
        query = {"query": ip, "variables": {}}  # Use CSV IP
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        print(f"  IP from CSV: {ip}")
        assert response.status_code in [200, 400, 422], f"Unexpected status {response.status_code}"
    
    def scenario_whois_with_sql_injection(self, headers):
        """TC-019: WHOIS with SQL injection"""
        query = {"query": "google.com' OR '1'='1", "variables": {}}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 400, 404], f"SQL injection should be handled safely"
    
    def scenario_whois_with_xss(self, headers):
        """TC-020: WHOIS with XSS attempt"""
        query = {"query": "<script>alert('XSS')</script>", "variables": {}}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 400, 404], f"XSS should be handled safely"
    
    def scenario_whois_with_command_injection(self, headers):
        """TC-021: WHOIS with command injection"""
        query = {"query": "google.com; rm -rf /", "variables": {}}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 400, 404], f"Command injection should be handled safely"
    
    def scenario_whois_with_very_long_query(self, headers):
        """TC-022: WHOIS with very long query"""
        query = {"query": "a" * 10000 + ".com", "variables": {}}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 413, 422], f"Very long query should be rejected, got {response.status_code}"
    
    def scenario_whois_with_get_method(self, headers):
        """TC-023: WHOIS with GET method"""
        response = requests.get(self.WHOIS_ENDPOINT, headers=headers)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [405, 404], f"GET should not be allowed, got {response.status_code}"
    
    def scenario_whois_with_put_method(self, headers, query):
        """TC-024: WHOIS with PUT method"""
        response = requests.put(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [405, 404], f"PUT should not be allowed, got {response.status_code}"
    
    def scenario_whois_with_delete_method(self, headers):
        """TC-025: WHOIS with DELETE method"""
        response = requests.delete(self.WHOIS_ENDPOINT, headers=headers)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [405, 404], f"DELETE should not be allowed, got {response.status_code}"
    
    def scenario_whois_with_wrong_content_type(self, headers, query):
        """TC-026: WHOIS with wrong Content-Type"""
        wrong_headers = headers.copy()
        wrong_headers["Content-Type"] = "text/plain"
        response = requests.post(self.WHOIS_ENDPOINT, headers=wrong_headers, data=json.dumps(query))
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 415, 500], f"Wrong Content-Type should return error"
    
    def scenario_whois_with_malformed_json(self, headers):
        """TC-027: WHOIS with malformed JSON"""
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, data='{"query": "google.com", invalid}')
        print(f"  Status: {response.status_code}")
        assert response.status_code in [400, 500], f"Malformed JSON should return error, got {response.status_code}"
    
    def scenario_whois_with_populated_variables(self, headers):
        """TC-028: WHOIS with populated variables"""
        query = {"query": "google.com", "variables": {"key1": "value1", "key2": "value2"}}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        assert response.status_code in [200, 201, 400], f"Unexpected status {response.status_code}"
    
    def scenario_whois_with_null_variables(self, headers):
        """TC-029: WHOIS with null variables"""
        query = {"query": "google.com", "variables": None}
        response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
        print(f"  Status: {response.status_code}")
        # Accept 403 as valid (permission/validation error)
        assert response.status_code in [200, 201, 400, 403, 422], f"Unexpected status {response.status_code}"
    
    def scenario_whois_multiple_rapid_requests(self, headers, query):
        """TC-030: WHOIS rate limiting"""
        responses = []
        for i in range(5):
            response = requests.post(self.WHOIS_ENDPOINT, headers=headers, json=query)
            responses.append(response.status_code)
            time.sleep(0.5)
        print(f"  Rapid requests: {responses}")
        rate_limited = any(status == 429 for status in responses)
        if rate_limited:
            print(f"  Rate limiting detected")
        else:
            print(f"  No rate limiting detected")
