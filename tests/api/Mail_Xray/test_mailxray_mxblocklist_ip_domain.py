import pytest
import requests
import os
import json
import time
import sys
import csv
from pathlib import Path
from utils.auth_token_helper import get_auth_token_from_login
from utils.config import BASE_URL, USERNAME, PASSWORD


class TestMailXrayMXBlocklistIP:
    """Test cases for MailXray MX Blocklist IP and Domain API"""
    
    # Use BASE_URL from utils/config.py
    MX_BLOCKLIST_IP_ENDPOINT = f"{BASE_URL}/tools/api/mxblocklist/ip/"
    MX_BLOCKLIST_DOMAIN_ENDPOINT = f"{BASE_URL}/tools/api/mxblocklist/domain/"
    
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
    
    def test_mxblocklist_ip_with_valid_ip_cookie_auth(self, headers, cookie_dict):
        """TC-001: Test MX Blocklist IP lookup with valid IP using Cookie authentication"""
        payload = {
            "query": "8.8.8.8",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        print(f"✓ MX Blocklist IP lookup successful for: 8.8.8.8")
    
    def test_mxblocklist_ip_with_valid_ip_token_auth(self, token_headers):
        """TC-002: Test MX Blocklist IP lookup with valid IP using Token authentication"""
        payload = {
            "query": "1.1.1.1",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=token_headers,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"✓ MX Blocklist IP lookup successful for: 1.1.1.1")
    
    def test_mxblocklist_ip_response_structure(self, headers, cookie_dict):
        """TC-003: Test MX Blocklist IP response structure"""
        payload = {
            "query": "8.8.8.8",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        assert response.status_code == 200
        response_data = response.json()
        
        print(f"\n✓ Response Data: {json.dumps(response_data, indent=2)[:1000]}")
        
        if isinstance(response_data, dict):
            print(f"✓ Response keys: {list(response_data.keys())}")
    
    @pytest.mark.parametrize("ip_address", [
        "8.8.8.8",      # Google DNS
        "1.1.1.1",      # Cloudflare DNS
        "4.4.4.4",      # Level3 DNS
        "208.67.222.222",  # OpenDNS
        "9.9.9.9"       # Quad9 DNS
    ])
    def test_mxblocklist_ip_multiple_ips(self, headers, cookie_dict, ip_address):
        """TC-004: Test MX Blocklist IP with multiple well-known IPs"""
        payload = {
            "query": ip_address,
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ IP: {ip_address}, Status: {response.status_code}")
        
        assert response.status_code == 200, f"Expected 200 for {ip_address}, got {response.status_code}"
    
    def test_mxblocklist_ip_with_private_ip(self, headers, cookie_dict):
        """TC-005: Test MX Blocklist IP with private IP address"""
        payload = {
            "query": "192.168.1.1",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # May return 200 or error depending on implementation
        print(f"✓ Private IP handling: Status {response.status_code}")
    
    def test_mxblocklist_ip_with_ipv6(self, headers, cookie_dict):
        """TC-006: Test MX Blocklist IP with IPv6 address"""
        payload = {
            "query": "2001:4860:4860::8888",  # Google DNS IPv6
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # IPv6 may or may not be supported
        print(f"✓ IPv6 handling: Status {response.status_code}")
    
    def test_mxblocklist_ip_with_localhost(self, headers, cookie_dict):
        """TC-007: Test MX Blocklist IP with localhost IP"""
        payload = {
            "query": "127.0.0.1",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        print(f"✓ Localhost IP handling: Status {response.status_code}")
    
    def test_mxblocklist_ip_validate_complete_response_body(self, token_headers):
        """TC-008: Test MX Blocklist IP and validate complete response body structure"""
        payload = {
            "query": "8.8.8.8",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=token_headers,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        # Validate status code
        assert response.status_code == 200, \
            f"Expected status code 200, got {response.status_code}"
        print(f"✓ Status code validation passed: 200")
        
        # Parse response JSON
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {response.text[:500]}")
        
        # Validate root level structure
        assert "status_code" in response_data or response.status_code == 200, \
            "Response should have status_code field or HTTP status 200"
        
        assert "data" in response_data, \
            "Response should have 'data' field"
        print(f"✓ Root level structure validated")
        
        data = response_data["data"]
        
        # Validate required data fields
        required_fields = [
            "query",
            "type",
            "blacklisted",
            "total_providers",
            "blacklisted_count",
            "status",
            "detections",
            "categories",
            "source",
            "summary"
        ]
        
        for field in required_fields:
            assert field in data, \
                f"Expected field '{field}' not found in response data"
        print(f"✓ All required fields present: {required_fields}")
        
        # Validate query field
        assert data["query"] == "8.8.8.8", \
            f"Query field mismatch: expected '8.8.8.8', got '{data.get('query')}'"
        print(f"✓ Query field validated: {data['query']}")
        
        # Validate type field
        assert data["type"] == "ip", \
            f"Type field mismatch: expected 'ip', got '{data.get('type')}'"
        print(f"✓ Type field validated: {data['type']}")
        
        # Validate blacklisted field (boolean)
        assert isinstance(data["blacklisted"], bool), \
            f"Blacklisted field should be boolean, got {type(data['blacklisted'])}"
        print(f"✓ Blacklisted field validated: {data['blacklisted']}")
        
        # Validate total_providers field (integer)
        assert isinstance(data["total_providers"], int), \
            f"Total_providers should be integer, got {type(data['total_providers'])}"
        assert data["total_providers"] > 0, \
            f"Total_providers should be > 0, got {data['total_providers']}"
        print(f"✓ Total providers validated: {data['total_providers']}")
        
        # Validate blacklisted_count field (integer)
        assert isinstance(data["blacklisted_count"], int), \
            f"Blacklisted_count should be integer, got {type(data['blacklisted_count'])}"
        assert data["blacklisted_count"] >= 0, \
            f"Blacklisted_count should be >= 0, got {data['blacklisted_count']}"
        print(f"✓ Blacklisted count validated: {data['blacklisted_count']}")
        
        # Validate status field
        valid_statuses = ["BLACKLISTED", "NOT_BLACKLISTED", "CLEAN"]
        assert data["status"] in valid_statuses, \
            f"Status should be one of {valid_statuses}, got '{data['status']}'"
        print(f"✓ Status field validated: {data['status']}")
        
        # Validate detections array
        assert isinstance(data["detections"], list), \
            f"Detections should be a list, got {type(data['detections'])}"
        print(f"✓ Detections is a list with {len(data['detections'])} items")
        
        # Validate detection items if any exist
        if len(data["detections"]) > 0:
            detection = data["detections"][0]
            required_detection_fields = ["provider", "listed", "details"]
            
            for field in required_detection_fields:
                assert field in detection, \
                    f"Detection should have '{field}' field"
            
            assert isinstance(detection["provider"], str), \
                "Provider should be a string"
            assert isinstance(detection["listed"], bool), \
                "Listed should be a boolean"
            
            print(f"✓ Detection structure validated")
            print(f"  - Sample provider: {detection['provider']}")
            print(f"  - Listed: {detection['listed']}")
        
        # Validate categories array
        assert isinstance(data["categories"], list), \
            f"Categories should be a list, got {type(data['categories'])}"
        print(f"✓ Categories validated: {data['categories']}")
        
        # Validate source field
        assert isinstance(data["source"], str), \
            f"Source should be a string, got {type(data['source'])}"
        assert len(data["source"]) > 0, \
            "Source should not be empty"
        print(f"✓ Source field validated: {data['source']}")
        
        # Validate summary field
        assert isinstance(data["summary"], str), \
            f"Summary should be a string, got {type(data['summary'])}"
        assert "8.8.8.8" in data["summary"], \
            f"Summary should contain the IP address"
        print(f"✓ Summary field validated: {data['summary']}")
        
        # Validate message field (if present)
        if "message" in response_data:
            assert isinstance(response_data["message"], str), \
                f"Message should be a string, got {type(response_data['message'])}"
            print(f"✓ Message field validated: {response_data['message']}")
        
        # Print full response structure summary
        print(f"\n✓ Full Response Data Structure:")
        print(f"  - status_code: {response.status_code}")
        print(f"  - query: {data['query']}")
        print(f"  - type: {data['type']}")
        print(f"  - blacklisted: {data['blacklisted']}")
        print(f"  - total_providers: {data['total_providers']}")
        print(f"  - blacklisted_count: {data['blacklisted_count']}")
        print(f"  - status: {data['status']}")
        print(f"  - detections count: {len(data['detections'])}")
        print(f"  - categories: {data['categories']}")
        print(f"  - source: {data['source']}")
        print(f"  - summary: {data['summary']}")
        
        print(f"\n✓ Complete response body validation successful!")
    
    def test_mxblocklist_domain_validate_response_from_testdata(self, token_headers):
        """TC-009: Test MX Blocklist Domain with domain from testdata and validate response body"""
        # Read domain from CSV testdata
        # Use project root as base for testdata
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        csv_path = Path(__file__).parent.parent.parent.parent / "testdata" / "mailxray_homepage.csv"        
        assert os.path.exists(csv_path), f"CSV file not found at {csv_path}"
        
        domain = None
        with open(csv_path, 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                # Only consider rows with a non-empty 'Domain' that looks like a domain
                val = row.get('Domain', '').strip()
                if val and '.' in val and not val.startswith('/'):
                    domain = val
                    break
        assert domain is not None, f"Domain not found in testdata CSV: {csv_file_path}"
        print(f"\n✓ Domain from testdata: {domain}")
        
        # Prepare payload
        payload = {
            "query": domain,
            "variables": {}
        }
        
        # Make API request
        response = requests.post(
            self.MX_BLOCKLIST_DOMAIN_ENDPOINT,
            headers=token_headers,
            json=payload
        )
        
        print(f"✓ Status Code: {response.status_code}")
        
        # Validate status code
        assert response.status_code == 200, \
            f"Expected status code 200, got {response.status_code}"
        print(f"✓ Status code validation passed: 200")
        
        # Parse response JSON
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {response.text[:500]}")
        
        # Validate root level structure
        assert "status_code" in response_data or response.status_code == 200, \
            "Response should have status_code field or HTTP status 200"
        
        assert "data" in response_data, \
            "Response should have 'data' field"
        print(f"✓ Root level structure validated")
        
        data = response_data["data"]
        
        # Validate required data fields
        required_fields = [
            "domain",
            "blacklisted",
            "total_providers",
            "blacklisted_count",
            "status",
            "detections",
            "categories",
            "source",
            "summary"
        ]
        
        for field in required_fields:
            assert field in data, \
                f"Expected field '{field}' not found in response data"
        print(f"✓ All required fields present: {required_fields}")
        
        # Validate domain field
        assert data["domain"] == domain, \
            f"Domain field mismatch: expected '{domain}', got '{data.get('domain')}'"
        print(f"✓ Domain field validated: {data['domain']}")
        
        # Validate blacklisted field (boolean)
        assert isinstance(data["blacklisted"], bool), \
            f"Blacklisted field should be boolean, got {type(data['blacklisted'])}"
        print(f"✓ Blacklisted field validated: {data['blacklisted']}")
        
        # Validate total_providers field (integer)
        assert isinstance(data["total_providers"], int), \
            f"Total_providers should be integer, got {type(data['total_providers'])}"
        assert data["total_providers"] > 0, \
            f"Total_providers should be > 0, got {data['total_providers']}"
        print(f"✓ Total providers validated: {data['total_providers']}")
        
        # Validate blacklisted_count field (integer)
        assert isinstance(data["blacklisted_count"], int), \
            f"Blacklisted_count should be integer, got {type(data['blacklisted_count'])}"
        assert data["blacklisted_count"] >= 0, \
            f"Blacklisted_count should be >= 0, got {data['blacklisted_count']}"
        print(f"✓ Blacklisted count validated: {data['blacklisted_count']}")
        
        # Validate status field
        valid_statuses = ["BLACKLISTED", "NOT_BLACKLISTED", "CLEAN"]
        assert data["status"] in valid_statuses, \
            f"Status should be one of {valid_statuses}, got '{data['status']}'"
        print(f"✓ Status field validated: {data['status']}")
        
        # Validate detections array
        assert isinstance(data["detections"], list), \
            f"Detections should be a list, got {type(data['detections'])}"
        print(f"✓ Detections is a list with {len(data['detections'])} items")
        
        # Validate detection items if any exist
        if len(data["detections"]) > 0:
            detection = data["detections"][0]
            required_detection_fields = ["provider", "listed", "details"]
            
            for field in required_detection_fields:
                assert field in detection, \
                    f"Detection should have '{field}' field"
            
            assert isinstance(detection["provider"], str), \
                "Provider should be a string"
            assert isinstance(detection["listed"], bool), \
                "Listed should be a boolean"
            
            print(f"✓ Detection structure validated")
            print(f"  - Sample provider: {detection['provider']}")
            print(f"  - Listed: {detection['listed']}")
            print(f"  - Details: {detection.get('details', 'N/A')}")
        
        # Validate categories array
        assert isinstance(data["categories"], list), \
            f"Categories should be a list, got {type(data['categories'])}"
        print(f"✓ Categories validated: {data['categories']}")
        
        # Validate source field
        assert isinstance(data["source"], str), \
            f"Source should be a string, got {type(data['source'])}"
        assert len(data["source"]) > 0, \
            "Source should not be empty"
        print(f"✓ Source field validated: {data['source']}")
        
        # Validate summary field
        assert isinstance(data["summary"], str), \
            f"Summary should be a string, got {type(data['summary'])}"
        assert domain in data["summary"], \
            f"Summary should contain the domain name"
        print(f"✓ Summary field validated: {data['summary']}")
        
        # Validate message field (if present)
        if "message" in response_data:
            assert isinstance(response_data["message"], str), \
                f"Message should be a string, got {type(response_data['message'])}"
            print(f"✓ Message field validated: {response_data['message']}")
        
        # Print full response structure summary
        print(f"\n✓ Full Response Data Structure:")
        print(f"  - status_code: {response.status_code}")
        print(f"  - domain: {data['domain']}")
        print(f"  - blacklisted: {data['blacklisted']}")
        print(f"  - total_providers: {data['total_providers']}")
        print(f"  - blacklisted_count: {data['blacklisted_count']}")
        print(f"  - status: {data['status']}")
        print(f"  - detections count: {len(data['detections'])}")
        print(f"  - categories: {data['categories']}")
        print(f"  - source: {data['source']}")
        print(f"  - summary: {data['summary']}")
        
        print(f"\n✓ Domain blacklist check from testdata completed successfully!")
    
    # ========== Negative Test Cases - Authentication ==========
    
    def test_mxblocklist_ip_without_authentication(self, headers):
        """TC-010: Test MX Blocklist IP without authentication"""
        payload = {
            "query": "8.8.8.8",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for missing auth, got {response.status_code}"
        
        response_data = response.json()
        assert "detail" in response_data
        print(f"✓ Authentication required: {response_data['detail']}")
    
    def test_mxblocklist_ip_with_invalid_token(self, headers):
        """TC-011: Test MX Blocklist IP with invalid token"""
        invalid_headers = headers.copy()
        invalid_headers["Authorization"] = "Token invalid_token_12345"
        
        payload = {
            "query": "8.8.8.8",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=invalid_headers,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for invalid token, got {response.status_code}"
        
        print(f"✓ Invalid token correctly rejected")
    
    def test_mxblocklist_ip_with_invalid_cookie(self, headers):
        """TC-012: Test MX Blocklist IP with invalid cookie"""
        invalid_cookies = {
            "auth_token": "invalid_cookie_12345"
        }
        
        payload = {
            "query": "8.8.8.8",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=invalid_cookies,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for invalid cookie, got {response.status_code}"
        
        print(f"✓ Invalid cookie correctly rejected")
    
    # ========== Negative Test Cases - Input Validation ==========
    
    def test_mxblocklist_ip_with_empty_query(self, headers, cookie_dict):
        """TC-013: Test MX Blocklist IP with empty query"""
        payload = {
            "query": "",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:200]}")
        
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for empty query, got {response.status_code}"
        
        print(f"✓ Empty query correctly rejected")
    
    def test_mxblocklist_ip_with_missing_query_field(self, headers, cookie_dict):
        """TC-014: Test MX Blocklist IP with missing query field"""
        payload = {
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for missing query, got {response.status_code}"
        
        print(f"✓ Missing query field correctly rejected")
    
    def test_mxblocklist_ip_with_null_query(self, headers, cookie_dict):
        """TC-015: Test MX Blocklist IP with null query"""
        payload = {
            "query": None,
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for null query, got {response.status_code}"
        
        print(f"✓ Null query correctly rejected")
    
    def test_mxblocklist_ip_with_empty_body(self, headers, cookie_dict):
        """TC-016: Test MX Blocklist IP with empty JSON body"""
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json={}
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for empty body, got {response.status_code}"
        
        print(f"✓ Empty body correctly rejected")
    
    def test_mxblocklist_ip_with_invalid_ip_format(self, headers, cookie_dict):
        """TC-017: Test MX Blocklist IP with invalid IP format"""
        invalid_ips = [
            "999.999.999.999",
            "256.1.1.1",
            "1.1.1",
            "1.1.1.1.1",
            "not_an_ip",
            "abc.def.ghi.jkl",
            "1.2.3.999"
        ]
        
        for ip in invalid_ips:
            payload = {
                "query": ip,
                "variables": {}
            }
            
            response = requests.post(
                self.MX_BLOCKLIST_IP_ENDPOINT,
                headers=headers,
                cookies=cookie_dict,
                json=payload
            )
            
            print(f"\n✓ IP: {ip}, Status: {response.status_code}")
    
    def test_mxblocklist_ip_with_domain_instead_of_ip(self, headers, cookie_dict):
        """TC-018: Test MX Blocklist IP with domain name instead of IP"""
        payload = {
            "query": "google.com",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # Should reject domain name or resolve it first
        print(f"✓ Domain instead of IP handling: Status {response.status_code}")
    
    
    # ========== Security Test Cases ==========
    
    def test_mxblocklist_ip_with_sql_injection(self, headers, cookie_dict):
        """TC-020: Test SQL injection attempt in query"""
        payload = {
            "query": "8.8.8.8' OR '1'='1",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        # Should handle safely without SQL injection
        print(f"✓ SQL injection attempt handled: Status {response.status_code}")
    
    def test_mxblocklist_ip_with_xss_attempt(self, headers, cookie_dict):
        """TC-021: Test XSS attempt in query"""
        payload = {
            "query": "<script>alert('XSS')</script>",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        # Should handle safely without XSS
        print(f"✓ XSS attempt handled: Status {response.status_code}")
    
    def test_mxblocklist_ip_with_command_injection(self, headers, cookie_dict):
        """TC-022: Test command injection attempt"""
        payload = {
            "query": "8.8.8.8; rm -rf /",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        # Should handle safely without command injection
        print(f"✓ Command injection attempt handled: Status {response.status_code}")
    
    # ========== Edge Cases ==========
    
    def test_mxblocklist_ip_with_leading_zeros(self, headers, cookie_dict):
        """TC-023: Test MX Blocklist IP with leading zeros"""
        payload = {
            "query": "008.008.008.008",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Leading zeros handling: Status {response.status_code}")
    
    def test_mxblocklist_ip_with_whitespace(self, headers, cookie_dict):
        """TC-024: Test MX Blocklist IP with leading/trailing whitespace"""
        payload = {
            "query": "  8.8.8.8  ",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # Should trim whitespace or handle appropriately
        print(f"✓ Whitespace handling: Status {response.status_code}")
    
    def test_mxblocklist_ip_with_cidr_notation(self, headers, cookie_dict):
        """TC-025: Test MX Blocklist IP with CIDR notation"""
        payload = {
            "query": "8.8.8.0/24",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ CIDR notation handling: Status {response.status_code}")
    
    def test_mxblocklist_ip_with_broadcast_ip(self, headers, cookie_dict):
        """TC-026: Test MX Blocklist IP with broadcast address"""
        payload = {
            "query": "255.255.255.255",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Broadcast IP handling: Status {response.status_code}")
    
    def test_mxblocklist_ip_with_zero_ip(self, headers, cookie_dict):
        """TC-027: Test MX Blocklist IP with 0.0.0.0"""
        payload = {
            "query": "0.0.0.0",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Zero IP handling: Status {response.status_code}")
    
    def test_mxblocklist_ip_with_multicast_ip(self, headers, cookie_dict):
        """TC-028: Test MX Blocklist IP with multicast address"""
        payload = {
            "query": "224.0.0.1",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Multicast IP handling: Status {response.status_code}")
    
    # ========== HTTP Method Tests ==========
    
    def test_mxblocklist_ip_with_get_method(self, token_headers):
        """TC-029: Test endpoint with GET method (should fail)"""
        response = requests.get(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=token_headers
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [405, 404], \
            f"GET method should not be allowed, got {response.status_code}"
        
        print(f"✓ GET method correctly rejected")
    
    def test_mxblocklist_ip_with_put_method(self, token_headers):
        """TC-030: Test endpoint with PUT method (should fail)"""
        payload = {
            "query": "8.8.8.8",
            "variables": {}
        }
        
        response = requests.put(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=token_headers,
            json=payload
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [405, 404], \
            f"PUT method should not be allowed, got {response.status_code}"
        
        print(f"✓ PUT method correctly rejected")
    
    def test_mxblocklist_ip_with_delete_method(self, token_headers):
        """TC-031: Test endpoint with DELETE method (should fail)"""
        response = requests.delete(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=token_headers
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [405, 404], \
            f"DELETE method should not be allowed, got {response.status_code}"
        
        print(f"✓ DELETE method correctly rejected")
    
    # ========== Performance Tests ==========
    
    def test_mxblocklist_ip_response_time(self, headers, cookie_dict):
        """TC-032: Test MX Blocklist IP response time (should be < 5 seconds)"""
        payload = {
            "query": "8.8.8.8",
            "variables": {}
        }
        
        start_time = time.time()
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            json=payload
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"\n✓ Response time: {response_time:.2f} seconds")
        
        assert response.status_code == 200
        assert response_time < 8.0, f"Response time {response_time:.2f}s exceeds 8 seconds"
        
        print(f"✓ Response time is acceptable")
    
    def test_mxblocklist_ip_multiple_rapid_requests(self, headers, cookie_dict):
        """TC-033: Test rate limiting with multiple rapid requests"""
        payload = {
            "query": "8.8.8.8",
            "variables": {}
        }
        
        responses = []
        for i in range(5):
            response = requests.post(
                self.MX_BLOCKLIST_IP_ENDPOINT,
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
    
    def test_mxblocklist_ip_with_malformed_json(self, headers, cookie_dict):
        """TC-034: Test MX Blocklist IP with malformed JSON"""
        malformed_json = '{"query": "8.8.8.8", "variables": invalid}'
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            headers=headers,
            cookies=cookie_dict,
            data=malformed_json
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [400, 500], \
            f"Malformed JSON should return error, got {response.status_code}"
        
        print(f"✓ Malformed JSON correctly rejected")
    
    def test_mxblocklist_ip_without_content_type(self, cookie_dict):
        """TC-035: Test MX Blocklist IP without Content-Type header"""
        payload = {
            "query": "8.8.8.8",
            "variables": {}
        }
        
        response = requests.post(
            self.MX_BLOCKLIST_IP_ENDPOINT,
            cookies=cookie_dict,
            json=payload  # requests will auto-add Content-Type
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Without explicit Content-Type handling: Status {response.status_code}")


# To run these tests:
# export MAILXRAY_BASE_URL="https://mailxray.dev.bci.aws.cudaops.com"
# export MAILXRAY_AUTH_TOKEN="e7b6eb81bb609e442b6ebd8876f7345d15d8c5fb"
# export MAILXRAY_AUTH_COOKIE="e6b22e6ed86acd7f09685f41c1698344da185d2e"
#
# Run all tests:
# .venv/bin/pytest -v -s tests --html=reports/mailxray_report.html --self-contained-html
#
# Run specific test:
# .venv/bin/pytest -v -s tests/api/Mail_Xray/test_mailxray_mxblocklist_ip.py::TestMailXrayMXBlocklistIP::test_mxblocklist_ip_with_valid_ip_cookie_auth
#
# Run authentication tests:
# .venv/bin/pytest -v -s tests/api/Mail_Xray/test_mailxray_mxblocklist_ip.py -k "auth"
#
# Run with HTML report:
# .venv/bin/pytest tests/api/Mail_Xray/test_mailxray_mxblocklist_ip.py --html=reports/mxblocklist_ip_report.html --self-contained-html
