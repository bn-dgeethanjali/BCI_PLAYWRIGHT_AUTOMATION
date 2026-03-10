import requests
import os

# Xray Cloud credentials
CLIENT_ID = os.getenv("XRAY_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("XRAY_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
PROJECT_KEY = os.getenv("XRAY_PROJECT_KEY", "BRTS")

# Xray API endpoints
AUTH_URL = "https://xray.cloud.getxray.app/api/v2/authenticate"
IMPORT_URL = f"https://xray.cloud.getxray.app/api/v2/import/execution/junit?projectKey={PROJECT_KEY}"

def get_xray_token():
    """Authenticate with Xray and get bearer token"""
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(AUTH_URL, json=payload)
    response.raise_for_status()
    return response.json().strip('"')

def upload_junit_results(file_path="junit-results.xml"):
    """Upload JUnit XML results to Jira Xray"""
    try:
        # Get authentication token
        print("Authenticating with Xray...")
        token = get_xray_token()
        
        # Upload results
        print(f"Uploading {file_path} to Xray...")
        headers = {"Authorization": f"Bearer {token}"}
        
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(IMPORT_URL, headers=headers, files=files)
        
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Successfully uploaded results to Xray!")
        print(f"Test Execution Key: {result.get('key', 'N/A')}")
        print(f"Test Execution ID: {result.get('id', 'N/A')}")
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error uploading to Xray: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        raise
    except FileNotFoundError:
        print(f"❌ Error: {file_path} not found!")
        raise

if __name__ == "__main__":
    upload_junit_results()
