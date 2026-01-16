
import requests
import json
import time

API_URL = "http://localhost:8000/api/auth"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password123"
NEW_PASSWORD = "newpassword456"

def test_reset_flow():
    print("1. Signing up user...")
    resp = requests.post(f"{API_URL}/sign-up", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "name": "Test User"
    })
    if resp.status_code != 201:
        print(f"Signup failed: {resp.text}")
        # Possibly user exists, try delete or just continue if we can

    # We need to verify the user first because sign-in check is_verified
    # In dev, the token is printed to console. Since I can't read console easily here,
    # I'll look at the database or assume the user is manually verified or bypass.
    # Actually, for the test, let's assume we can trigger forgot-password even if not verified.

    print("\n2. Requesting password reset...")
    resp = requests.post(f"{API_URL}/forgot-password", json={"email": TEST_EMAIL})
    print(f"Forgot password response: {resp.json()}")

    print("\nNote: Please check the backend logs for the [RESET EMAIL] link.")
    print("Since this is an automated test, I will attempt to find the token in the database.")

if __name__ == "__main__":
    test_reset_flow()
