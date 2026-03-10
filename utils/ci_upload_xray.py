#!/usr/bin/env python3
"""
CI/CD friendly script - uses environment variables for credentials
Works with GitHub Actions, Jenkins, GitLab CI, etc.
"""
import os
import base64
import requests
import json


class CIConfig:
    """Configuration handler for CI/CD environments"""
    
    @staticmethod
    def get_jira_credentials():
        """Get JIRA credentials from environment variables"""
        email = os.getenv('JIRA_USER_EMAIL')
        token = os.getenv('JIRA_API_TOKEN')
        
        if not email or not token:
            raise ValueError("JIRA_USER_EMAIL and JIRA_API_TOKEN must be set")
        
        return email, token
    
    @staticmethod
    def get_xray_credentials():
        """Get Xray credentials from environment variables"""
        client_id = os.getenv('XRAY_CLIENT_ID')
        client_secret = os.getenv('XRAY_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            raise ValueError("XRAY_CLIENT_ID and XRAY_CLIENT_SECRET must be set")
        
        return client_id, client_secret


def authenticate_xray():
    """Authenticate with Xray and get bearer token"""
    client_id, client_secret = CIConfig.get_xray_credentials()
    
    url = "https://xray.cloud.getxray.app/api/v2/authenticate"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    return response.json().strip('"')


def import_junit_to_xray(file_path, project_key, test_plan_key=None):
    """Import JUnit XML results to Xray"""
    token = authenticate_xray()
    
    url = f"https://xray.cloud.getxray.app/api/v2/import/execution/junit?projectKey={project_key}"
    if test_plan_key:
        url += f"&testPlanKey={test_plan_key}"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(file_path, 'rb') as f:
        response = requests.post(url, headers=headers, files={'file': f})
    
    response.raise_for_status()
    result = response.json()
    
    print(f"✅ Results imported to Xray")
    print(f"Test Execution Key: {result.get('key')}")
    
    return result


def attach_file_to_jira(issue_key, file_path):
    """Attach file to Jira issue"""
    email, token = CIConfig.get_jira_credentials()
    jira_url = os.getenv('JIRA_BASE_URL', 'https://cuda.atlassian.net')
    
    url = f"{jira_url}/rest/api/3/issue/{issue_key}/attachments"
    headers = {"X-Atlassian-Token": "no-check"}
    auth = (email, token)
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, headers=headers, auth=auth, files=files)
    
    response.raise_for_status()
    
    print(f"✅ File attached to {issue_key}")
    return response.json()


def main():
    """Main CI/CD workflow"""
    # Configuration
    project_key = os.getenv('XRAY_PROJECT_KEY', 'BNRTS')
    test_plan_key = os.getenv('XRAY_TEST_PLAN_KEY')
    junit_file = 'junit-results.xml'
    results_file = 'tests/ui/results.json'
    
    try:
        # Step 1: Import results to Xray
        print("📤 Importing test results to Xray...")
        xray_result = import_junit_to_xray(junit_file, project_key, test_plan_key)
        
        issue_key = xray_result.get('key')
        
        # Step 2: Attach results file
        if issue_key and os.path.exists(results_file):
            print(f"📎 Attaching results to {issue_key}...")
            attach_file_to_jira(issue_key, results_file)
        
        print(f"🎉 Success! View at: https://cuda.atlassian.net/browse/{issue_key}")
        
        # Export for next steps
        if os.getenv('GITHUB_ENV'):
            with open(os.getenv('GITHUB_ENV'), 'a') as f:
                f.write(f"TEST_EXECUTION_KEY={issue_key}\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
