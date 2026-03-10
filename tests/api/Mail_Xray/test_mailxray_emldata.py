import pytest
import requests
import os
import json
import sys
from io import BytesIO
import tempfile
from pathlib import Path

# Add workspace root to path
workspace_root = str(Path(__file__).parent.parent.parent.parent)
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

# Import credentials from utils/config.py
from utils.config import BASE_URL, USERNAME, PASSWORD


class TestMailXrayEMLData:
    """Test cases for MailXray EML Data Upload API"""
    
    # Use BASE_URL from utils/config.py
    EMLDATA_ENDPOINT = f"{BASE_URL}/tools/api/emldata/"
    
    # Sample EML content for testing
    SAMPLE_EML_CONTENT = """From: sender@example.com
To: recipient@example.com
Subject: Test Email
Date: Wed, 12 Feb 2026 10:00:00 +0000
Message-ID: <test123@example.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

This is a test email body.
"""

    SAMPLE_EML_WITH_ATTACHMENT = """From: sender@example.com
To: recipient@example.com
Subject: Test Email with Attachment
Date: Wed, 12 Feb 2026 10:00:00 +0000
Message-ID: <test456@example.com>
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="boundary123"

--boundary123
Content-Type: text/plain; charset=UTF-8

This is the email body.

--boundary123
Content-Type: application/pdf; name="document.pdf"
Content-Disposition: attachment; filename="document.pdf"
Content-Transfer-Encoding: base64

JVBERi0xLjQKJeLjz9MKM...
--boundary123--
"""
    
    @pytest.fixture
    def auth_token(self):
        """Fixture to provide authentication token dynamically from login API"""
        from utils.auth_token_helper import get_auth_token_from_login
        return get_auth_token_from_login()
    
    @pytest.fixture
    def auth_cookie(self, auth_token):
        """Fixture to provide authentication cookie (same as token)"""
        return auth_token
    
    @pytest.fixture
    def token_headers(self, auth_token):
        """Fixture to provide headers with Token authentication"""
        return {
            "Authorization": f"Token {auth_token}"
        }
    @pytest.fixture
    def cookie_dict(self, auth_cookie):
        """Fixture to provide cookies for authentication"""
        return {
            "auth_token": auth_cookie
        }
    
    @pytest.fixture
    def sample_eml_file(self):
        """Fixture to create a temporary EML file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.eml', delete=False) as f:
            f.write(self.SAMPLE_EML_CONTENT)
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    @pytest.fixture
    def sample_eml_with_attachment(self):
        """Fixture to create a temporary EML file with attachment"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.eml', delete=False) as f:
            f.write(self.SAMPLE_EML_WITH_ATTACHMENT)
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    # ========== Positive Test Cases ==========
    
    def test_upload_eml_with_token_auth(self, token_headers, sample_eml_file):
        """TC-001: Test EML file upload with Token authentication"""
        with open(sample_eml_file, 'rb') as f:
            files = {'eml': ('test.eml', f, 'message/rfc822')}
            
            response = requests.post(
                self.EMLDATA_ENDPOINT,
                headers=token_headers,
                files=files
            )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        # Accept various success codes
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ EML file uploaded successfully with Token auth")
    
    def test_upload_eml_with_cookie_auth(self, cookie_dict, sample_eml_file):
        """TC-002: Test EML file upload with Cookie authentication"""
        with open(sample_eml_file, 'rb') as f:
            files = {'eml': ('test.eml', f, 'message/rfc822')}
            
            response = requests.post(
                self.EMLDATA_ENDPOINT,
                cookies=cookie_dict,
                files=files
            )
        
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ EML file uploaded successfully with Cookie auth")
    
    def test_upload_eml_with_both_auth_methods(self, token_headers, cookie_dict, sample_eml_file):
        """TC-003: Test EML file upload with both Token and Cookie authentication"""
        with open(sample_eml_file, 'rb') as f:
            files = {'eml': ('test.eml', f, 'message/rfc822')}
            
            response = requests.post(
                self.EMLDATA_ENDPOINT,
                headers=token_headers,
                cookies=cookie_dict,
                files=files
            )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ EML file uploaded successfully with both auth methods")
    
    def test_upload_eml_with_attachment(self, token_headers, sample_eml_with_attachment):
        """TC-004: Test EML file with attachment upload"""
        with open(sample_eml_with_attachment, 'rb') as f:
            files = {'eml': ('email_with_attachment.eml', f, 'message/rfc822')}
            
            response = requests.post(
                self.EMLDATA_ENDPOINT,
                headers=token_headers,
                files=files
            )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ EML file with attachment uploaded successfully")
    
    def test_upload_eml_response_structure(self, token_headers, sample_eml_file):
        """TC-005: Test EML upload response structure"""
        with open(sample_eml_file, 'rb') as f:
            files = {'eml': ('test.eml', f, 'message/rfc822')}
            
            response = requests.post(
                self.EMLDATA_ENDPOINT,
                headers=token_headers,
                files=files
            )
        
        assert response.status_code in [200, 201]
        
        # Try to parse response as JSON
        try:
            response_data = response.json()
            print(f"\n✓ Response Data: {json.dumps(response_data, indent=2)[:500]}")
            
            # Common fields to check
            if isinstance(response_data, dict):
                print(f"✓ Response is a dictionary with keys: {list(response_data.keys())}")
        except:
            print(f"\n✓ Response is not JSON: {response.text[:200]}")
    
    def test_upload_eml_from_real_file(self, token_headers):
        """TC-006: Test uploading EML file dynamically from environment variable or testdata folder"""
        # Try to get EML file path from environment variable
        eml_path = os.getenv("EML_FILE_PATH")
        
        # If not set, try to find .eml files in testdata directory
        if not eml_path:
            testdata_dir = Path(__file__).parent.parent.parent.parent / "testdata"
            if testdata_dir.exists():
                eml_files = list(testdata_dir.glob("*.eml"))
                if eml_files:
                    eml_path = str(eml_files[0])
                    print(f"\n✓ Using EML file from testdata: {eml_path}")
        
        # Skip test if no EML file found
        if not eml_path or not os.path.exists(eml_path):
            pytest.skip("EML file not found. Set EML_FILE_PATH environment variable or place .eml file in testdata folder")
        
        print(f"\n✓ Testing with EML file: {eml_path}")
        
        with open(eml_path, 'rb') as f:
            files = {'eml': (os.path.basename(eml_path), f, 'message/rfc822')}
            
            response = requests.post(
                self.EMLDATA_ENDPOINT,
                headers=token_headers,
                files=files
            )
        
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.text[:500]}")
        
        assert response.status_code in [200, 201], \
            f"Expected 200 or 201, got {response.status_code}"
        
        print(f"✓ Real EML file uploaded successfully")
    
    # ========== Negative Test Cases - Authentication ==========
    
    def test_upload_eml_without_authentication(self, sample_eml_file):
        """TC-007: Test EML upload without any authentication"""
        with open(sample_eml_file, 'rb') as f:
            files = {'eml': ('test.eml', f, 'message/rfc822')}
            
            response = requests.post(
                self.EMLDATA_ENDPOINT,
                files=files
            )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        # Should return 401 or 403
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for missing auth, got {response.status_code}"
        
        response_data = response.json()
        assert "detail" in response_data
        print(f"✓ Authentication required: {response_data['detail']}")
    
    def test_upload_eml_with_invalid_token(self, sample_eml_file):
        """TC-008: Test EML upload with invalid token"""
        invalid_headers = {
            "Authorization": "Token invalid_token_12345"
        }
        
        with open(sample_eml_file, 'rb') as f:
            files = {'eml': ('test.eml', f, 'message/rfc822')}
            
            response = requests.post(
                self.EMLDATA_ENDPOINT,
                headers=invalid_headers,
                files=files
            )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for invalid token, got {response.status_code}"
        
        print(f"✓ Invalid token correctly rejected")
    
    def test_upload_eml_with_invalid_cookie(self, sample_eml_file):
        """TC-009: Test EML upload with invalid cookie"""
        invalid_cookies = {
            "auth_token": "invalid_cookie_12345"
        }
        
        with open(sample_eml_file, 'rb') as f:
            files = {'eml': ('test.eml', f, 'message/rfc822')}
            
            response = requests.post(
                self.EMLDATA_ENDPOINT,
                cookies=invalid_cookies,
                files=files
            )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for invalid cookie, got {response.status_code}"
        
        print(f"✓ Invalid cookie correctly rejected")
    
    def test_upload_eml_with_malformed_auth_header(self, sample_eml_file):
        """TC-010: Test EML upload with malformed Authorization header"""
        malformed_headers = {
            "Authorization": "InvalidFormat 12345"
        }
        
        with open(sample_eml_file, 'rb') as f:
            files = {'eml': ('test.eml', f, 'message/rfc822')}
            
            response = requests.post(
                self.EMLDATA_ENDPOINT,
                headers=malformed_headers,
                files=files
            )
        
        print(f"\n✓ Status Code: {response.status_code}")
        
        assert response.status_code in [401, 403], \
            f"Expected 401 or 403 for malformed auth, got {response.status_code}"
        
        print(f"✓ Malformed auth header correctly rejected")
    
 