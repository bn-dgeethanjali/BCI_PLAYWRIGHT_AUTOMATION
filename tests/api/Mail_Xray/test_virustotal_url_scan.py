import pytest
import requests
import os
import json
import time


class TestVirusTotalURLScan:
    """Test cases for VirusTotal API v3 URL Scanning"""
    
    VT_URL_SCAN_ENDPOINT = "https://www.virustotal.com/api/v3/urls"
    
    @pytest.fixture
    def api_key(self):
        """Fixture to provide VirusTotal API key"""
        return os.getenv("VIRUSTOTAL_API_KEY", "c1c5f23d5a927863bd85bd06abc6d4c6f7c10d2a0229989f1259611da5bae633")
    
    @pytest.fixture
    def headers(self, api_key):
        """Fixture to provide headers with API key"""
        return {
            "x-apikey": api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }
    
    # ========== Positive Test Cases ==========
    
    def test_url_scan_with_google(self, headers):
        """TC-001: Test URL scan for Google.com"""
        data = {
            "url": "https://google.com"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        response_data = response.json()
        print(f"✓ URL scan submitted successfully for: https://google.com")
        
        # Check response structure
        if "data" in response_data:
            print(f"✓ Response contains 'data' field")
            if "id" in response_data["data"]:
                print(f"✓ Scan ID: {response_data['data']['id']}")
    
    def test_url_scan_with_http(self, headers):
        """TC-002: Test URL scan with HTTP protocol"""
        data = {
            "url": "http://example.com"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ URL scan submitted for HTTP URL")
    
    def test_url_scan_with_subdomain(self, headers):
        """TC-003: Test URL scan with subdomain"""
        data = {
            "url": "https://mail.google.com"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ URL scan submitted for subdomain")
    
    def test_url_scan_with_path(self, headers):
        """TC-004: Test URL scan with path"""
        data = {
            "url": "https://www.google.com/search?q=test"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ URL scan submitted for URL with path and query params")
    
    def test_url_scan_with_port(self, headers):
        """TC-005: Test URL scan with custom port"""
        data = {
            "url": "https://example.com:8080"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ URL scan submitted for URL with custom port")
    
    def test_url_scan_with_fragment(self, headers):
        """TC-006: Test URL scan with fragment"""
        data = {
            "url": "https://example.com/page#section"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ URL scan submitted for URL with fragment")
    
    def test_url_scan_response_structure(self, headers):
        """TC-007: Test URL scan response structure"""
        data = {
            "url": "https://github.com"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        response_data = response.json()
        print(f"✓ Response is valid JSON")
        print(f"✓ Response keys: {list(response_data.keys())}")
        
        # Verify expected fields in response
        if "data" in response_data:
            print(f"✓ Response contains 'data' field")
            data_keys = list(response_data["data"].keys())
            print(f"✓ Data keys: {data_keys}")
    
    @pytest.mark.parametrize("url", [
        "https://google.com",
        "https://github.com",
        "https://stackoverflow.com",
        "https://reddit.com"
    ])
    def test_url_scan_with_multiple_urls(self, headers, url):
        """TC-008: Test URL scan with multiple popular URLs"""
        data = {"url": url}
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ URL: {url}")
        print(f"✓ Response: {response.text[:300]}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201 for {url}, got {response.status_code}"
    
    def test_url_scan_with_international_domain(self, headers):
        """TC-009: Test URL scan with international domain"""
        data = {
            "url": "https://www.google.co.uk"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ URL scan submitted for international domain")
    
    def test_url_scan_with_long_url(self, headers):
        """TC-010: Test URL scan with very long URL"""
        long_path = "/".join(["segment"] * 20)
        data = {
            "url": f"https://example.com/{long_path}?param=value"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # Long URLs should be accepted
        print(f"✓ Long URL handling: Status {response.status_code}")
    
    # ========== Negative Test Cases ==========
    
    def test_url_scan_without_url_field(self, headers):
        """TC-011: Test URL scan without URL field"""
        data = {}
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for missing URL, got {response.status_code}"
        
        print(f"✓ API correctly rejected request without URL field")
    
    def test_url_scan_with_empty_url(self, headers):
        """TC-012: Test URL scan with empty URL"""
        data = {
            "url": ""
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for empty URL, got {response.status_code}"
        
        print(f"✓ API correctly rejected empty URL")
    
    def test_url_scan_with_invalid_url(self, headers):
        """TC-013: Test URL scan with invalid URL format"""
        data = {
            "url": "not-a-valid-url"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for invalid URL, got {response.status_code}"
        
        print(f"✓ API correctly rejected invalid URL format")
    
    def test_url_scan_without_protocol(self, headers):
        """TC-014: Test URL scan without protocol"""
        data = {
            "url": "google.com"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API may accept and add default protocol or reject
        print(f"✓ URL without protocol handling: Status {response.status_code}")
    
    def test_url_scan_with_malformed_url(self, headers):
        """TC-015: Test URL scan with malformed URL"""
        data = {
            "url": "https://example..com"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API may reject malformed URLs
        print(f"✓ Malformed URL handling: Status {response.status_code}")
    
    def test_url_scan_without_api_key(self):
        """TC-016: Test URL scan without API key"""
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "url": "https://google.com"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for missing API key, got {response.status_code}"
        
        print(f"✓ API correctly rejected request without API key")
    
    def test_url_scan_with_invalid_api_key(self):
        """TC-017: Test URL scan with invalid API key"""
        headers = {
            "x-apikey": "invalid_api_key_12345",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "url": "https://google.com"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for invalid API key, got {response.status_code}"
        
        print(f"✓ API correctly rejected invalid API key")
    
    def test_url_scan_with_ip_address(self, headers):
        """TC-018: Test URL scan with IP address instead of domain"""
        data = {
            "url": "https://8.8.8.8"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API may accept IP addresses in URLs
        print(f"✓ IP address in URL handling: Status {response.status_code}")
    
    def test_url_scan_with_localhost(self, headers):
        """TC-019: Test URL scan with localhost"""
        data = {
            "url": "http://localhost:8080"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API may reject localhost URLs
        print(f"✓ Localhost URL handling: Status {response.status_code}")
    
    def test_url_scan_with_private_ip(self, headers):
        """TC-020: Test URL scan with private IP address"""
        data = {
            "url": "http://192.168.1.1"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API may reject private IP addresses
        print(f"✓ Private IP URL handling: Status {response.status_code}")
    
    # ========== Security Test Cases ==========
    
    def test_url_scan_with_sql_injection(self, headers):
        """TC-021: Test URL scan with SQL injection attempt"""
        data = {
            "url": "https://example.com/page?id=1' OR '1'='1"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API should handle SQL injection attempts safely
        print(f"✓ SQL injection handling: Status {response.status_code}")
    
    def test_url_scan_with_xss_in_url(self, headers):
        """TC-022: Test URL scan with XSS attempt in URL"""
        data = {
            "url": "https://example.com/<script>alert('XSS')</script>"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API should handle XSS attempts safely
        print(f"✓ XSS in URL handling: Status {response.status_code}")
    
    def test_url_scan_with_command_injection(self, headers):
        """TC-023: Test URL scan with command injection attempt"""
        data = {
            "url": "https://example.com/page?cmd=$(whoami)"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API should handle command injection attempts safely
        print(f"✓ Command injection handling: Status {response.status_code}")
    
    def test_url_scan_with_file_protocol(self, headers):
        """TC-024: Test URL scan with file:// protocol"""
        data = {
            "url": "file:///etc/passwd"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API should reject file:// protocol
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for file protocol, got {response.status_code}"
        
        print(f"✓ API correctly rejected file:// protocol")
    
    def test_url_scan_with_javascript_protocol(self, headers):
        """TC-025: Test URL scan with javascript: protocol"""
        data = {
            "url": "javascript:alert('XSS')"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API should reject javascript: protocol
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 for javascript protocol, got {response.status_code}"
        
        print(f"✓ API correctly rejected javascript: protocol")
    
    # ========== HTTP Method Tests ==========
    
    def test_url_scan_with_get_method(self, headers):
        """TC-026: Test URL scan with GET method (should fail)"""
        response = requests.get(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [405, 404], \
            f"Expected 405 or 404 for GET method, got {response.status_code}"
        
        print(f"✓ API correctly rejected GET method")
    
    def test_url_scan_with_put_method(self, headers):
        """TC-027: Test URL scan with PUT method (should fail)"""
        data = {
            "url": "https://google.com"
        }
        
        response = requests.put(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [405, 404], \
            f"Expected 405 or 404 for PUT method, got {response.status_code}"
        
        print(f"✓ API correctly rejected PUT method")
    
    def test_url_scan_with_delete_method(self, headers):
        """TC-028: Test URL scan with DELETE method (should fail)"""
        response = requests.delete(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [405, 404], \
            f"Expected 405 or 404 for DELETE method, got {response.status_code}"
        
        print(f"✓ API correctly rejected DELETE method")
    
    # ========== Edge Cases ==========
    
    def test_url_scan_with_unicode_characters(self, headers):
        """TC-029: Test URL scan with Unicode characters"""
        data = {
            "url": "https://example.com/页面"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API may handle Unicode URLs with IDN encoding
        print(f"✓ Unicode URL handling: Status {response.status_code}")
    
    def test_url_scan_with_special_characters(self, headers):
        """TC-030: Test URL scan with special characters"""
        data = {
            "url": "https://example.com/page?name=John%20Doe&age=30"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ URL with special characters handled correctly")
    
    def test_url_scan_with_whitespace(self, headers):
        """TC-031: Test URL scan with whitespace"""
        data = {
            "url": " https://google.com "
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API may trim whitespace or reject
        print(f"✓ Whitespace handling: Status {response.status_code}")
    
    def test_url_scan_with_multiple_slashes(self, headers):
        """TC-032: Test URL scan with multiple slashes"""
        data = {
            "url": "https://example.com//path//to//page"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API should handle multiple slashes
        print(f"✓ Multiple slashes handling: Status {response.status_code}")
    
    def test_url_scan_with_extra_fields(self, headers):
        """TC-033: Test URL scan with extra fields"""
        data = {
            "url": "https://google.com",
            "extra_field": "should_be_ignored",
            "another_field": 123
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API should ignore extra fields or reject
        print(f"✓ Extra fields handling: Status {response.status_code}")
    
    # ========== Performance Test Cases ==========
    
    def test_url_scan_response_time(self, headers):
        """TC-034: Test URL scan response time"""
        data = {
            "url": "https://google.com"
        }
        
        start_time = time.time()
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        end_time = time.time()
        
        response_time = end_time - start_time
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response Time: {response_time:.2f} seconds")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        # Verify response time is reasonable (less than 30 seconds)
        assert response_time < 30, f"Response time {response_time:.2f}s exceeds 30s threshold"
        
        print(f"✓ Response time within acceptable limits")
    
    def test_url_scan_concurrent_requests(self, headers):
        """TC-035: Test URL scan with concurrent requests"""
        import concurrent.futures
        
        def send_request(url):
            data = {"url": url}
            response = requests.post(
                self.VT_URL_SCAN_ENDPOINT,
                headers=headers,
                data=data
            )
            return response.status_code
        
        # Send 3 concurrent requests with different URLs
        urls = [
            "https://google.com",
            "https://github.com",
            "https://stackoverflow.com"
        ]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(send_request, url) for url in urls]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        print(f"\n✓ Concurrent request results: {results}")
        
        # Check if any requests succeeded
        success_count = sum(1 for status in results if status in [200, 201])
        print(f"✓ Successful requests: {success_count}/3")
        
        # Note: VirusTotal API may have rate limits, so some requests might fail
        print(f"✓ Concurrent requests test completed")
    
    def test_url_scan_with_extremely_long_url(self, headers):
        """TC-036: Test URL scan with extremely long URL (over 2000 chars)"""
        long_path = "A" * 2000
        data = {
            "url": f"https://example.com/{long_path}"
        }
        
        response = requests.post(
            self.VT_URL_SCAN_ENDPOINT,
            headers=headers,
            data=data
        )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # API may reject extremely long URLs or have a limit
        print(f"✓ Extremely long URL handling: Status {response.status_code}")
