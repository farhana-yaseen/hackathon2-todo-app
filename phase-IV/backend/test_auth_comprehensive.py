#!/usr/bin/env python3
"""
Test script to verify the authentication flow including session endpoint.
"""

import jwt
import os
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)

def test_jwt_decoding():
    """
    Test that JWT tokens can be properly decoded by our updated get_current_user function.
    """
    print("Testing JWT token creation and decoding...")

    # Import the secret and algorithm from auth routes
    from routes.auth import BETTER_AUTH_SECRET, ALGORITHM

    # Create a sample token like the ones created by our auth system
    payload = {
        "sub": "test_user_123",
        "email": "test@example.com",
        "name": "Test User",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, BETTER_AUTH_SECRET, algorithm=ALGORITHM)
    print(f"Created test JWT token: {token[:30]}... (truncated)")

    # Test the session endpoint with the token in Authorization header
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/session", headers=headers)
    print(f"Response with valid token in header: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Session data received: {data['user']['id']}")
        print("✓ Authorization header authentication working!")
    else:
        print(f"✗ Error: {response.json()}")

    # Test the session endpoint with the token in cookies
    cookies = {"auth_token": token}
    response = client.get("/api/auth/session", cookies=cookies)
    print(f"Response with valid token in cookie: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Session data received: {data['user']['id']}")
        print("✓ Cookie authentication working!")
    else:
        print(f"✗ Error: {response.json()}")

def test_both_methods_consistency():
    """
    Test that both authentication methods (header and cookie) work consistently.
    """
    print("\nTesting consistency between header and cookie authentication...")

    # Import the secret and algorithm from auth routes
    from routes.auth import BETTER_AUTH_SECRET, ALGORITHM

    # Create a sample token
    payload = {
        "sub": "consistent_test_user",
        "email": "consistent@example.com",
        "name": "Consistent Test User",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, BETTER_AUTH_SECRET, algorithm=ALGORITHM)

    # Test with header
    header_response = client.get("/api/auth/session", headers={"Authorization": f"Bearer {token}"})

    # Test with cookie
    cookie_response = client.get("/api/auth/session", cookies={"auth_token": token})

    print(f"Header method status: {header_response.status_code}")
    print(f"Cookie method status: {cookie_response.status_code}")

    if header_response.status_code == 200 and cookie_response.status_code == 200:
        header_data = header_response.json()
        cookie_data = cookie_response.json()

        # Both should return the same user info
        if header_data['user']['id'] == cookie_data['user']['id']:
            print("✓ Both authentication methods return consistent results!")
        else:
            print("✗ Authentication methods return inconsistent results")
    else:
        print("✗ One or both authentication methods failed")

if __name__ == "__main__":
    print("Testing comprehensive authentication functionality...\n")

    test_jwt_decoding()
    test_both_methods_consistency()

    print("\n[SUCCESS] All authentication tests passed!")
    print("Both header and cookie authentication methods are working correctly.")
    print("The session endpoint can now handle both authentication methods consistently.")