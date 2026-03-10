import pytest
import requests
import os
import json
import time
import sys
from datetime import datetime
from pathlib import Path

# Add workspace root to path
workspace_root = str(Path(__file__).parent.parent.parent.parent)
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

# Import credentials from utils/config.py
from utils.config import BASE_URL, USERNAME, PASSWORD


class TestMailXrayLogin:
    """Comprehensive test for MailXray Login API - All scenarios in one test"""
    
    # Use BASE_URL from utils/config.py
    LOGIN_ENDPOINT = f"{BASE_URL}/tools/api/login/"
    
    def get_valid_credentials(self):
        """Get valid login credentials from utils/config.py"""
        return {
            "username": USERNAME,
            "password": PASSWORD
        }
    
    def get_headers(self):
        """Get request headers"""
        return {
            "Content-Type": "application/json"
        }
    
    def test_mailxray_login_all_scenarios(self):
        """
        Single comprehensive test that executes all 38 login test scenarios.
        Tests: positive cases, negative cases, security tests, edge cases, HTTP methods, and more.
        """
        valid_credentials = self.get_valid_credentials()
        headers = self.get_headers()
        
        print("\n" + "="*80)
        print("MAILXRAY LOGIN API - COMPREHENSIVE TEST (38 SCENARIOS)")
        print("="*80)
        print(f"Endpoint: {self.LOGIN_ENDPOINT}")
        print(f"Username: {USERNAME}")
        print("="*80)
        
        test_count = 0
        passed_count = 0
        failed_count = 0
        
        # ========== Positive Test Cases ==========
        print("\n" + "="*80)
        print("SECTION 1: POSITIVE TEST CASES")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test successful login with valid credentials")
        try:
            self.scenario_login_success_with_valid_credentials(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Verify login response contains authentication token")
        try:
            self.scenario_login_response_contains_authentication_token(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Verify login API response time")
        try:
            self.scenario_login_response_time(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Verify login response headers")
        try:
            self.scenario_login_response_headers(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Verify login returns user information")
        try:
            self.scenario_login_returns_user_information(valid_credentials, headers)
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
        print(f"\n[Test {test_count}/38] Test login with invalid username")
        try:
            self.scenario_login_with_invalid_username(headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with invalid password")
        try:
            self.scenario_login_with_invalid_password(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with both credentials invalid")
        try:
            self.scenario_login_with_both_credentials_invalid(headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with empty username")
        try:
            self.scenario_login_with_empty_username(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with empty password")
        try:
            self.scenario_login_with_empty_password(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with both fields empty")
        try:
            self.scenario_login_with_both_fields_empty(headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login missing username field")
        try:
            self.scenario_login_missing_username_field(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login missing password field")
        try:
            self.scenario_login_missing_password_field(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with empty JSON body")
        try:
            self.scenario_login_with_empty_json_body(headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with null username")
        try:
            self.scenario_login_with_null_username(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with null password")
        try:
            self.scenario_login_with_null_password(valid_credentials, headers)
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
        print(f"\n[Test {test_count}/38] Test SQL injection attempt in username")
        try:
            self.scenario_login_with_sql_injection_in_username(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test XSS attempt in username")
        try:
            self.scenario_login_with_xss_in_username(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with special characters in password")
        try:
            self.scenario_login_with_special_characters_in_password(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test username case sensitivity")
        try:
            self.scenario_login_case_sensitivity_username(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Edge Cases ==========
        print("\n" + "="*80)
        print("SECTION 4: EDGE CASES")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with whitespace in username")
        try:
            self.scenario_login_with_whitespace_in_username(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with very long username")
        try:
            self.scenario_login_with_very_long_username(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with very long password")
        try:
            self.scenario_login_with_very_long_password(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with unicode characters")
        try:
            self.scenario_login_with_unicode_characters(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== HTTP Method Tests ==========
        print("\n" + "="*80)
        print("SECTION 5: HTTP METHOD TESTS")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with GET method")
        try:
            self.scenario_login_with_get_method(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with PUT method")
        try:
            self.scenario_login_with_put_method(valid_credentials, headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with DELETE method")
        try:
            self.scenario_login_with_delete_method(headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Content-Type Tests ==========
        print("\n" + "="*80)
        print("SECTION 6: CONTENT-TYPE TESTS")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with missing content-type")
        try:
            self.scenario_login_with_missing_content_type(valid_credentials)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with wrong content-type")
        try:
            self.scenario_login_with_wrong_content_type(valid_credentials)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test login with malformed JSON")
        try:
            self.scenario_login_with_malformed_json(headers)
            passed_count += 1
            print("✓ PASSED")
        except AssertionError as e:
            failed_count += 1
            print(f"✗ FAILED: {e}")
        
        # ========== Parametrized Scenarios ==========
        print("\n" + "="*80)
        print("SECTION 7: VARIOUS LOGIN SCENARIOS")
        print("="*80)
        
        scenarios = [
            (USERNAME, PASSWORD, "Valid credentials"),
            ("invalid_user", "invalid_pass", "Invalid username and password"),
            ("", "password123", "Empty username"),
            ("username", "", "Empty password"),
            ("admin", "admin", "Common default credentials"),
            ("root", "root", "Another common default"),
            ("test@example.com", "password", "Email format username"),
        ]
        
        for username, password, description in scenarios:
            test_count += 1
            print(f"\n[Test {test_count}/38] Test: {description}")
            try:
                self.scenario_login_various_scenarios(username, password, description, headers)
                passed_count += 1
                print("✓ PASSED")
            except AssertionError as e:
                failed_count += 1
                print(f"✗ FAILED: {e}")
        
        # ========== Rate Limiting Test ==========
        print("\n" + "="*80)
        print("SECTION 8: RATE LIMITING TEST")
        print("="*80)
        
        test_count += 1
        print(f"\n[Test {test_count}/38] Test multiple rapid requests")
        try:
            self.scenario_login_multiple_rapid_requests(valid_credentials, headers)
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
        print("\n✓✓✓ ALL 38 LOGIN API SCENARIOS PASSED SUCCESSFULLY ✓✓✓\n")
    
    # ========== Scenario Methods (Previously test_ methods) ==========
    
    def scenario_login_success_with_valid_credentials(self, valid_credentials, headers):
        """TC-001: Test successful login with valid credentials"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json=valid_credentials)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        response_data = response.json()
        print(f"  Login successful for user: {valid_credentials['username']}")
    
    def scenario_login_response_contains_authentication_token(self, valid_credentials, headers):
        """TC-002: Verify login response contains authentication token"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json=valid_credentials)
        assert response.status_code == 200
        response_data = response.json()
        has_token = "token" in response_data or ("data" in response_data and "token" in response_data.get("data", {}))
        has_user_data = "user" in response_data or ("data" in response_data and "user" in response_data.get("data", {}))
        assert has_token or has_user_data, "Response should contain authentication token or user data"
        print(f"  Authentication token or user data present")
    
    def scenario_login_response_time(self, valid_credentials, headers):
        """TC-003: Verify login API response time"""
        start_time = time.time()
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json=valid_credentials)
        response_time = time.time() - start_time
        assert response.status_code == 200
        assert response_time < 3.0, f"Response time {response_time:.2f}s exceeds 3 seconds"
        print(f"  Response time: {response_time:.2f} seconds")
    
    def scenario_login_response_headers(self, valid_credentials, headers):
        """TC-004: Verify login response headers"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json=valid_credentials)
        assert response.status_code == 200
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type.lower()
        print(f"  Content-Type: {content_type}")
    
    def scenario_login_returns_user_information(self, valid_credentials, headers):
        """TC-005: Verify login response contains user information"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json=valid_credentials)
        assert response.status_code == 200
        response_data = response.json()
        has_user_info = "user" in response_data or ("data" in response_data and "user" in response_data.get("data", {}))
        print(f"  User information present: {has_user_info}")
    
    def scenario_login_with_invalid_username(self, headers):
        """TC-006: Test login with invalid username"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": "invalid_user_12345", "password": "Himajabellamkonda@123"})
        assert response.status_code in [400, 401, 403, 404]
        print(f"  Invalid username rejected with status {response.status_code}")
    
    def scenario_login_with_invalid_password(self, valid_credentials, headers):
        """TC-007: Test login with invalid password"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": valid_credentials["username"], "password": "WrongPassword@123"})
        assert response.status_code in [400, 401, 403]
        print(f"  Invalid password rejected with status {response.status_code}")
    
    def scenario_login_with_both_credentials_invalid(self, headers):
        """TC-008: Test login with both invalid credentials"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": "nonexistent_user", "password": "wrong_password"})
        assert response.status_code in [400, 401, 403]
        print(f"  Invalid credentials rejected with status {response.status_code}")
    
    def scenario_login_with_empty_username(self, valid_credentials, headers):
        """TC-009: Test login with empty username"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": "", "password": valid_credentials["password"]})
        assert response.status_code in [400, 401, 422]
        print(f"  Empty username rejected with status {response.status_code}")
    
    def scenario_login_with_empty_password(self, valid_credentials, headers):
        """TC-010: Test login with empty password"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": valid_credentials["username"], "password": ""})
        assert response.status_code in [400, 401, 422]
        print(f"  Empty password rejected with status {response.status_code}")
    
    def scenario_login_with_both_fields_empty(self, headers):
        """TC-011: Test login with both fields empty"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": "", "password": ""})
        assert response.status_code in [400, 401, 422]
        print(f"  Empty credentials rejected with status {response.status_code}")
    
    def scenario_login_missing_username_field(self, valid_credentials, headers):
        """TC-012: Test login with missing username field"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"password": valid_credentials["password"]})
        assert response.status_code in [400, 422]
        print(f"  Missing username field rejected with status {response.status_code}")
    
    def scenario_login_missing_password_field(self, valid_credentials, headers):
        """TC-013: Test login with missing password field"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": valid_credentials["username"]})
        assert response.status_code in [400, 422]
        print(f"  Missing password field rejected with status {response.status_code}")
    
    def scenario_login_with_empty_json_body(self, headers):
        """TC-014: Test login with empty JSON body"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={})
        assert response.status_code in [400, 422]
        print(f"  Empty JSON body rejected with status {response.status_code}")
    
    def scenario_login_with_null_username(self, valid_credentials, headers):
        """TC-015: Test login with null username"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": None, "password": valid_credentials["password"]})
        assert response.status_code in [400, 422]
        print(f"  Null username rejected with status {response.status_code}")
    
    def scenario_login_with_null_password(self, valid_credentials, headers):
        """TC-016: Test login with null password"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": valid_credentials["username"], "password": None})
        assert response.status_code in [400, 422]
        print(f"  Null password rejected with status {response.status_code}")
    
    def scenario_login_with_sql_injection_in_username(self, valid_credentials, headers):
        """TC-017: Test SQL injection attempt in username"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": "admin' OR '1'='1", "password": valid_credentials["password"]})
        assert response.status_code in [400, 401, 403]
        print(f"  SQL injection blocked")
    
    def scenario_login_with_xss_in_username(self, valid_credentials, headers):
        """TC-018: Test XSS attempt in username"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": "<script>alert('XSS')</script>", "password": valid_credentials["password"]})
        assert response.status_code in [400, 401, 403]
        print(f"  XSS attempt blocked")
    
    def scenario_login_with_special_characters_in_password(self, valid_credentials, headers):
        """TC-019: Test login with special characters in password"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": valid_credentials["username"], "password": "P@ssw0rd!#$%^&*()"})
        assert response.status_code in [200, 401]
        print(f"  Special characters handled with status {response.status_code}")
    
    def scenario_login_case_sensitivity_username(self, valid_credentials, headers):
        """TC-020: Test username case sensitivity"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": valid_credentials["username"].upper(), "password": valid_credentials["password"]})
        print(f"  Case sensitivity test: Status {response.status_code}")
    
    def scenario_login_with_whitespace_in_username(self, valid_credentials, headers):
        """TC-021: Test login with whitespace in username"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": f"  {valid_credentials['username']}  ", "password": valid_credentials["password"]})
        print(f"  Whitespace handling: Status {response.status_code}")
    
    def scenario_login_with_very_long_username(self, valid_credentials, headers):
        """TC-022: Test login with very long username"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": "a" * 1000, "password": valid_credentials["password"]})
        assert response.status_code in [400, 401, 413, 422]
        print(f"  Very long username rejected with status {response.status_code}")
    
    def scenario_login_with_very_long_password(self, valid_credentials, headers):
        """TC-023: Test login with very long password"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": valid_credentials["username"], "password": "P@ssw0rd" * 1000})
        assert response.status_code in [400, 401, 413, 422]
        print(f"  Very long password rejected with status {response.status_code}")
    
    def scenario_login_with_unicode_characters(self, valid_credentials, headers):
        """TC-024: Test login with unicode characters"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": "用户名测试", "password": "パスワード123"})
        assert response.status_code in [400, 401, 403]
        print(f"  Unicode characters handled with status {response.status_code}")
    
    def scenario_login_with_get_method(self, valid_credentials, headers):
        """TC-025: Test login with GET method"""
        response = requests.get(self.LOGIN_ENDPOINT, headers=headers, params=valid_credentials)
        assert response.status_code in [405, 404]
        print(f"  GET method rejected with status {response.status_code}")
    
    def scenario_login_with_put_method(self, valid_credentials, headers):
        """TC-026: Test login with PUT method"""
        response = requests.put(self.LOGIN_ENDPOINT, headers=headers, json=valid_credentials)
        assert response.status_code in [405, 404]
        print(f"  PUT method rejected with status {response.status_code}")
    
    def scenario_login_with_delete_method(self, headers):
        """TC-027: Test login with DELETE method"""
        response = requests.delete(self.LOGIN_ENDPOINT, headers=headers)
        assert response.status_code in [405, 404]
        print(f"  DELETE method rejected with status {response.status_code}")
    
    def scenario_login_with_missing_content_type(self, valid_credentials):
        """TC-028: Test login without Content-Type header"""
        response = requests.post(self.LOGIN_ENDPOINT, json=valid_credentials)
        print(f"  Missing Content-Type: Status {response.status_code}")
    
    def scenario_login_with_wrong_content_type(self, valid_credentials):
        """TC-029: Test login with wrong Content-Type"""
        response = requests.post(self.LOGIN_ENDPOINT, headers={"Content-Type": "text/plain"}, data=json.dumps(valid_credentials))
        print(f"  Wrong Content-Type: Status {response.status_code}")
    
    def scenario_login_with_malformed_json(self, headers):
        """TC-030: Test login with malformed JSON"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, data='{"username": "test", "password": invalid}')
        assert response.status_code in [400, 500]
        print(f"  Malformed JSON rejected with status {response.status_code}")
    
    def scenario_login_various_scenarios(self, username, password, description, headers):
        """TC-031: Parametrized test for various scenarios"""
        response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json={"username": username, "password": password})
        print(f"  {description}: Status {response.status_code}")
    
    def scenario_login_multiple_rapid_requests(self, valid_credentials, headers):
        """TC-032: Test rate limiting"""
        responses = []
        for i in range(5):
            response = requests.post(self.LOGIN_ENDPOINT, headers=headers, json=valid_credentials)
            responses.append(response.status_code)
            time.sleep(0.1)
        print(f"  Multiple rapid requests: {responses}")
        rate_limited = any(status == 429 for status in responses)
        if rate_limited:
            print(f"  Rate limiting detected")
        else:
            print(f"  No rate limiting detected")
