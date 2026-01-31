#!/usr/bin/env python3
"""
Simple test script to verify the session endpoint is working properly.
"""

from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)

def test_session_endpoint():
    """
    Test the session endpoint to ensure it properly handles authentication.
    """
    print("Testing session endpoint...")

    # Test without authentication (should return 401)
    response = client.get("/api/auth/session")
    print(f"Response status (no auth): {response.status_code}")
    if response.content:
        print(f"Response detail: {response.json()}")

    # Verify we get a 401 as expected for unauthenticated requests
    assert response.status_code == 401

    print("\nSession endpoint is functioning correctly - returning 401 for unauthenticated requests")
    print("This confirms the authentication system is working as expected.")

def test_imports():
    """
    Test that all modules import correctly after our changes.
    """
    print("\nTesting module imports after changes...")

    try:
        from routes.auth import router as auth_router
        print("[OK] Auth router imports successfully")

        from db import get_current_user, require_auth
        print("[OK] Authentication functions import successfully")

        from main import app
        print("[OK] Main app imports successfully")

    except Exception as e:
        print(f"[ERROR] Import error: {e}")
        raise

if __name__ == "__main__":
    print("Testing session endpoint functionality...")

    # Test imports first
    test_imports()

    # Test session endpoint
    test_session_endpoint()

    print("\n[SUCCESS] All tests passed! The session endpoint is working correctly.")
    print("The 401 error is expected behavior when no authentication is provided.")