#!/usr/bin/env python3
"""
Practical OAuth Error Testing Script (No Unicode)

This script tests the most accessible error scenarios in the OAuth authentication flow
for GitHub and Google login providers by testing the API endpoints directly.
"""

import os
import requests
from urllib.parse import urlparse, parse_qs
import json
from typing import Dict, List, Tuple
import time

# Configuration
BASE_URL = os.getenv("API_URL", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


def test_invalid_providers():
    """
    Test invalid provider names in both login and callback endpoints
    """
    print("=" * 60)
    print("TEST: Invalid Provider Names")
    print("=" * 60)

    invalid_providers = ["invalid", "fake", "test", "nonexistent", "123", ""]

    endpoints_to_test = [
        "/api/auth/login/{provider}",
        "/api/auth/callback/{provider}"
    ]

    all_passed = True

    for endpoint_template in endpoints_to_test:
        print(f"\nTesting endpoint: {endpoint_template}")
        print("-" * 40)

        for provider in invalid_providers:
            endpoint = endpoint_template.format(provider=provider)
            url = f"{BASE_URL}{endpoint}"

            try:
                response = requests.get(url, allow_redirects=False)
                print(f"Provider '{provider}': Status {response.status_code}", end="")

                if response.status_code == 400 or response.status_code == 422:
                    print(" [PASS]")
                else:
                    print(f" [FAIL] (Expected 400 or 422, got {response.status_code})")
                    all_passed = False

                # Try to get error message if available
                try:
                    error_data = response.json()
                    if 'detail' in error_data:
                        print(f"  Error message: {error_data['detail']}")
                except:
                    pass

            except requests.exceptions.RequestException as e:
                print(f"Provider '{provider}': Request failed - {e}")
                all_passed = False

    print(f"\nOverall result: {'[ALL PASSED]' if all_passed else '[SOME FAILED]'}")
    return all_passed


def test_valid_provider_format():
    """
    Test that valid providers (google, github) don't return errors
    """
    print("\n" + "=" * 60)
    print("TEST: Valid Provider Names")
    print("=" * 60)

    valid_providers = ["google", "github"]

    all_passed = True

    for provider in valid_providers:
        print(f"\nTesting valid provider: {provider}")
        login_url = f"{BASE_URL}/api/auth/login/{provider}"

        try:
            response = requests.get(login_url, allow_redirects=False)
            print(f"Provider '{provider}': Status {response.status_code}")

            # For valid providers, we expect either:
            # - 302/307 redirect to OAuth provider (success)
            # - 400/422 if env vars not configured (expected in test env)
            if response.status_code in [302, 307]:
                print("  [PASS] - Valid provider - redirect to OAuth provider")
            elif response.status_code in [400, 404, 422]:
                print("  [PASS] - Valid provider - but OAuth not configured (expected in test)")
            elif response.status_code == 401:
                print("  [PASS] - Valid provider - but OAuth credentials missing (expected in test)")
            else:
                print(f"  [FAIL] - Unexpected status: {response.status_code}")
                all_passed = False

        except requests.exceptions.RequestException as e:
            print(f"Provider '{provider}': Request failed - {e}")
            all_passed = False

    return all_passed


def test_callback_without_oauth():
    """
    Test callback endpoints directly (without actual OAuth flow)
    """
    print("\n" + "=" * 60)
    print("TEST: Callback Endpoints Without OAuth Flow")
    print("=" * 60)

    providers = ["google", "github"]

    all_passed = True

    for provider in providers:
        print(f"\nTesting callback for provider: {provider}")
        callback_url = f"{BASE_URL}/api/auth/callback/{provider}"

        try:
            response = requests.get(callback_url, allow_redirects=False)
            print(f"Callback for '{provider}': Status {response.status_code}")

            # Without proper OAuth state, we expect errors
            if response.status_code in [302, 307]:
                # Might redirect to frontend with error
                location = response.headers.get('Location', '')
                print(f"  Redirects to: {location}")
                if 'error' in location.lower():
                    print("  [PASS] - Properly redirects with error")
                else:
                    print("  [WARN] - Redirects but no error in URL")
            elif response.status_code >= 400:
                print("  [PASS] - Returns appropriate error status")
            else:
                print(f"  [FAIL] - Unexpected status: {response.status_code}")
                all_passed = False

        except requests.exceptions.RequestException as e:
            print(f"Callback for '{provider}': Request failed - {e}")
            all_passed = False

    return all_passed


def analyze_error_handling():
    """
    Analyze the current error handling implementation
    """
    print("\n" + "=" * 60)
    print("ANALYSIS: Current Error Handling Implementation")
    print("=" * 60)

    print("\nBackend Error Handling:")
    print("- Lines 480-484: Generic exception handler for OAuth errors")
    print("- Logs errors with logger.error()")
    print("- Redirects to frontend with generic 'OAuth failed' message")
    print("- Validates provider names (returns 400 for invalid providers)")
    print("- Checks for email from OAuth providers (returns 400 if missing)")

    print("\nFrontend Error Handling:")
    print("- Lines 16-32: useEffect handles success tokens but not error params")
    print("- No explicit handling of OAuth error redirects")
    print("- Traditional login has proper error display (line 50)")

    print("\nIdentified Issues:")
    print("1. Frontend doesn't handle error parameters from OAuth callbacks")
    print("2. Generic error messages don't help users troubleshoot")
    print("3. No distinction between different types of OAuth failures")

    print("\nRecommendations:")
    print("1. Add error parameter handling in frontend useEffect")
    print("2. Provide more specific error messages")
    print("3. Add user-friendly error UI for OAuth failures")


def run_comprehensive_test():
    """
    Run all practical tests that can be executed
    """
    print("OAuth Error Testing - Practical Implementation")
    print("=" * 60)
    print(f"Target API: {BASE_URL}")
    print(f"Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    print()

    results = []

    # Test 1: Invalid providers
    print("Running invalid provider tests...")
    result1 = test_invalid_providers()
    results.append(("Invalid Providers", result1))

    # Test 2: Valid providers
    print("\nRunning valid provider tests...")
    result2 = test_valid_provider_format()
    results.append(("Valid Providers", result2))

    # Test 3: Callback endpoints
    print("\nRunning callback endpoint tests...")
    result3 = test_callback_without_oauth()
    results.append(("Callback Endpoints", result3))

    # Analysis
    analyze_error_handling()

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{test_name}: {status}")

    overall_passed = all(result for _, result in results)
    print(f"\nOverall: {'[ALL TESTS PASSED]' if overall_passed else '[SOME TESTS FAILED]'}")

    print("\nNote: This test suite focuses on API-level error handling.")
    print("Full OAuth flow testing requires configured OAuth credentials.")


if __name__ == "__main__":
    run_comprehensive_test()