#!/usr/bin/env python3
"""
OAuth Error Testing Script for GitHub and Google Login

This script tests various error scenarios in the OAuth authentication flow
for GitHub and Google login providers.
"""

import os
import requests
from urllib.parse import urlparse, parse_qs
import json
from typing import Dict, List, Tuple

# Configuration
BASE_URL = os.getenv("API_URL", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


def test_missing_oauth_credentials():
    """
    Test scenario: OAuth providers not configured due to missing environment variables
    """
    print("=" * 60)
    print("TEST 1: Missing OAuth Credentials")
    print("=" * 60)

    # This test assumes we temporarily unset the env vars to simulate the issue
    # In practice, you'd need to restart the server with missing env vars
    print("Scenario: OAuth providers not registered due to missing environment variables")
    print("- If GOOGLE_CLIENT_ID/GITHUB_CLIENT_ID not set, providers won't be available")
    print("- Clicking social login buttons would result in 'Invalid provider' error")
    print("[MANUAL TEST]: Verify environment variables are properly set")
    print()


def test_invalid_provider():
    """
    Test scenario: Invalid provider parameter in OAuth endpoints
    """
    print("=" * 60)
    print("TEST 2: Invalid Provider Parameter")
    print("=" * 60)

    invalid_providers = ["invalid", "fake", "nonexistent", "test"]

    for provider in invalid_providers:
        print(f"Testing invalid provider: {provider}")

        # Test login endpoint
        login_url = f"{BASE_URL}/api/auth/login/{provider}"
        try:
            response = requests.get(login_url, allow_redirects=False)
            print(f"  GET {login_url}")
            print(f"  Status: {response.status_code}")
            if response.status_code == 400:
                print("  ✓ Correctly returns 400 for invalid provider")
            else:
                print(f"  ⚠ Unexpected status: {response.status_code}")

            if response.status_code == 422:  # Validation error
                print("  ✓ Correctly validates provider parameter")

        except Exception as e:
            print(f"  Error testing {login_url}: {e}")

        # Test callback endpoint
        callback_url = f"{BASE_URL}/api/auth/callback/{provider}"
        try:
            response = requests.get(callback_url, allow_redirects=False)
            print(f"  GET {callback_url}")
            print(f"  Status: {response.status_code}")
            if response.status_code == 400:
                print("  ✓ Correctly returns 400 for invalid provider in callback")
            else:
                print(f"  ⚠ Unexpected status: {response.status_code}")

        except Exception as e:
            print(f"  Error testing {callback_url}: {e}")

        print()


def test_github_no_email_scenario():
    """
    Test scenario: Simulate GitHub not returning email address
    """
    print("=" * 60)
    print("TEST 3: Missing Email from OAuth Provider")
    print("=" * 60)

    print("Scenario: OAuth provider doesn't return email address")
    print("- Backend should return 400 with 'Email not provided by OAuth provider'")
    print("- This is difficult to test without mocking the OAuth service")
    print("[MANUAL TEST]:")
    print("  1. Mock GitHub/Google API to return user info without email")
    print("  2. Trigger OAuth flow")
    print("  3. Verify 400 error with appropriate message")
    print()


def test_oauth_network_error():
    """
    Test scenario: Network issues during OAuth flow
    """
    print("=" * 60)
    print("TEST 4: Network Issues During OAuth Flow")
    print("=" * 60)

    print("Scenario: Network problems during OAuth handshake")
    print("- Backend should catch exceptions and redirect with error")
    print("- Difficult to test without simulating network conditions")
    print("[MANUAL TEST]:")
    print("  1. Use network simulation tools to introduce delays/errors")
    print("  2. Monitor backend logs for error handling")
    print("  3. Verify proper error redirection")
    print()


def test_malformed_oauth_response():
    """
    Test scenario: Malformed response from OAuth provider
    """
    print("=" * 60)
    print("TEST 5: Malformed OAuth Response")
    print("=" * 60)

    print("Scenario: OAuth provider returns unexpected data format")
    print("- Backend should handle parsing errors gracefully")
    print("- This requires mocking the OAuth service response")
    print("[MANUAL TEST]:")
    print("  1. Mock GitHub/Google API to return malformed JSON/data")
    print("  2. Trigger OAuth flow")
    print("  3. Verify error handling and user-friendly message")
    print()


def test_user_denied_consent():
    """
    Test scenario: User denies OAuth consent
    """
    print("=" * 60)
    print("TEST 6: User Denies OAuth Consent")
    print("=" * 60)

    print("Scenario: User rejects OAuth permission during the flow")
    print("- OAuth library should handle denial and trigger error flow")
    print("- Backend should redirect with appropriate error message")
    print("[MANUAL TEST]:")
    print("  1. Initiate OAuth flow in browser")
    print("  2. At OAuth consent screen, deny permissions/cancel")
    print("  3. Verify redirect to frontend with error parameter")
    print()


def test_frontend_error_display():
    """
    Test scenario: Frontend handling of OAuth errors
    """
    print("=" * 60)
    print("TEST 7: Frontend Error Display")
    print("=" * 60)

    print("Scenario: OAuth flow returns error to frontend")
    print("- Frontend should display error message to user")
    print("- Currently, frontend only handles success tokens in useEffect")
    print("[MANUAL TEST]:")
    print("  1. Manually navigate to sign-in page with error parameter:")
    print(f"     {FRONTEND_URL}/auth/sign-in?error=OAuth failed")
    print("  2. Check if error message is displayed appropriately")
    print("  3. Verify error handling in frontend component")
    print()


def run_all_tests():
    """
    Execute all OAuth error tests
    """
    print("OAuth Error Testing Suite")
    print("=" * 60)
    print(f"Base API URL: {BASE_URL}")
    print(f"Frontend URL: {FRONTEND_URL}")
    print()

    test_missing_oauth_credentials()
    test_invalid_provider()
    test_github_no_email_scenario()
    test_oauth_network_error()
    test_malformed_oauth_response()
    test_user_denied_consent()
    test_frontend_error_display()

    print("=" * 60)
    print("OAuth Error Testing Complete")
    print("Note: Some tests require manual verification or mocking")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()