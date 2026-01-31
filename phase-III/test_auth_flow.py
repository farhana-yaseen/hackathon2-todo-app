"""
Test script to verify authentication flow after fixing auth errors.
This script tests the key authentication endpoints and ensures they work properly.
"""

import requests
import json
import time
import uuid

# Configuration
BASE_URL = "http://localhost:8000"  # Adjust this to your backend URL
TEST_EMAIL = f"test_{uuid.uuid4()}@example.com"
TEST_PASSWORD = "testpassword123"
TEST_NAME = "Test User"

print("Testing Authentication Flow After Fixes")
print("="*50)

# Test 1: Check if backend is running
print("\n1. Checking backend health...")
try:
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print(f"   [OK] Backend is healthy: {response.json()}")
    else:
        print(f"   [FAIL] Backend health check failed: {response.status_code}")
except Exception as e:
    print(f"   [FAIL] Backend not accessible: {e}")
    exit(1)

# Test 2: Signup
print(f"\n2. Testing user signup with email: {TEST_EMAIL}...")
try:
    signup_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "name": TEST_NAME
    }

    response = requests.post(f"{BASE_URL}/api/auth/sign-up", json=signup_data)

    if response.status_code == 201:
        print("   [OK] Signup successful")
        # Check if token is in response
        if "token" in response.json():
            print("   [OK] Token received in response")
        else:
            print("   [WARN] No token in response")

        # Check if auth_token cookie is set
        cookies = response.cookies
        if "auth_token" in cookies:
            print("   [OK] auth_token cookie set")
            AUTH_TOKEN = cookies["auth_token"]
        else:
            print("   [WARN] auth_token cookie not set")
            AUTH_TOKEN = None

    else:
        print(f"   [FAIL] Signup failed: {response.status_code} - {response.text}")

except Exception as e:
    print(f"   [FAIL] Signup test failed: {e}")

# Test 3: Signin
print(f"\n3. Testing user signin...")
try:
    signin_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }

    response = requests.post(f"{BASE_URL}/api/auth/sign-in", json=signin_data)

    if response.status_code == 200:
        print("   [OK] Signin successful")

        # Check if auth_token cookie is set
        cookies = response.cookies
        if "auth_token" in cookies:
            print("   [OK] auth_token cookie set")
            AUTH_TOKEN = cookies["auth_token"]
        else:
            print("   [WARN] auth_token cookie not set")

        # Also check if token is in response
        if "token" in response.json():
            print("   [OK] Token received in response")
    else:
        print(f"   [FAIL] Signin failed: {response.status_code} - {response.text}")

except Exception as e:
    print(f"   [FAIL] Signin test failed: {e}")

# Test 4: Session endpoint
print(f"\n4. Testing session endpoint...")
try:
    # Use the auth token from cookies
    headers = {}
    cookies = {}
    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
        cookies["auth_token"] = AUTH_TOKEN

    response = requests.get(f"{BASE_URL}/api/auth/session", headers=headers, cookies=cookies)

    if response.status_code == 200:
        session_data = response.json()
        print("   [OK] Session endpoint accessible")
        print(f"   [OK] User: {session_data.get('user', {}).get('name', 'Unknown')}")
        print(f"   [OK] Email: {session_data.get('user', {}).get('email', 'Unknown')}")
    else:
        print(f"   [FAIL] Session endpoint failed: {response.status_code} - {response.text}")

except Exception as e:
    print(f"   [FAIL] Session test failed: {e}")

# Test 5: Profile endpoint
print(f"\n5. Testing profile endpoint...")
try:
    headers = {}
    cookies = {}
    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
        cookies["auth_token"] = AUTH_TOKEN

    response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers, cookies=cookies)

    if response.status_code == 200:
        profile_data = response.json()
        print("   [OK] Profile endpoint accessible")
        print(f"   [OK] User ID: {profile_data.get('id', 'Unknown')}")
        print(f"   [OK] Name: {profile_data.get('name', 'Unknown')}")
    else:
        print(f"   [FAIL] Profile endpoint failed: {response.status_code} - {response.text}")

except Exception as e:
    print(f"   [FAIL] Profile test failed: {e}")

# Test 6: Check cookie attributes (manually inspect response headers)
print(f"\n6. Testing cookie attributes...")
try:
    signin_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }

    response = requests.post(f"{BASE_URL}/api/auth/sign-in", json=signin_data)

    if response.status_code == 200:
        # Check Set-Cookie header
        set_cookie_header = response.headers.get('Set-Cookie', '')
        print(f"   Set-Cookie header: {set_cookie_header}")

        # Check if the cookie contains expected attributes
        if 'HttpOnly' in set_cookie_header:
            print("   [OK] HttpOnly attribute present")
        else:
            print("   [WARN] HttpOnly attribute missing")

        if 'Secure' in set_cookie_header:
            print("   [OK] Secure attribute present")
        else:
            print("   [WARN] Secure attribute missing (may be expected in non-HTTPS environment)")

        if 'SameSite=None' in set_cookie_header or 'samesite=none' in set_cookie_header.lower():
            print("   [OK] SameSite=None attribute present")
        else:
            print("   [WARN] SameSite=None attribute missing")

    else:
        print(f"   [FAIL] Cookie attribute test failed: {response.status_code}")

except Exception as e:
    print(f"   [FAIL] Cookie attribute test failed: {e}")

print(f"\nAuthentication flow testing completed!")
print("="*50)
print("Note: For production testing, ensure your backend is served over HTTPS")
print("as the cookie attributes may behave differently in HTTP vs HTTPS.")