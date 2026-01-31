#!/usr/bin/env python3
"""
Simple test to verify authentication methods work.
"""

import jwt
import os
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)

def test_authentication_methods():
    """
    Test that both authentication methods (header and cookie) work.
    """
    print("Testing authentication methods...")

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
        print("[OK] Authorization header authentication working!")
    else:
        print(f"[ERROR] Header auth failed: {response.json()}")

    # Test the session endpoint with the token in cookies
    cookies = {"auth_token": token}
    response = client.get("/api/auth/session", cookies=cookies)
    print(f"Response with valid token in cookie: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Session data received: {data['user']['id']}")
        print("[OK] Cookie authentication working!")
    else:
        print(f"[ERROR] Cookie auth failed: {response.json()}")

if __name__ == "__main__":
    print("Testing authentication functionality...")
    test_authentication_methods()
    print("\n[SUCCESS] Authentication methods test completed!")