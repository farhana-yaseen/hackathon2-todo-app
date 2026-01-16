#!/usr/bin/env python3
"""
Test script to verify the OAuth cookie fix.
This script tests that the auth cookie is properly set during OAuth callback.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL
from backend.routes.auth import auth_callback
from sqlmodel import Session
import os

async def test_oauth_callback_sets_cookie():
    """
    Test that the OAuth callback function properly sets the auth cookie on the redirect response.
    """
    print("Testing OAuth callback cookie setting...")

    # Mock the request object
    mock_request = AsyncMock()
    mock_request.url_for = MagicMock(return_value=URL("http://testserver/callback/google"))

    # Mock the database session
    mock_db_session = MagicMock(spec=Session)

    # Mock the OAuth provider response (simulating Google OAuth)
    import sys
    from unittest.mock import patch

    # Temporarily set environment variables for testing
    os.environ["FRONTEND_URL"] = "http://localhost:3000"
    os.environ["BETTER_AUTH_SECRET"] = "test-secret"

    # Mock the OAuth token response
    with patch('backend.routes.auth.oauth') as mock_oauth:
        mock_google = MagicMock()
        mock_token = {'userinfo': {'email': 'test@example.com', 'name': 'Test User'}}
        mock_google.authorize_access_token = AsyncMock(return_value=mock_token)

        mock_oauth.google = mock_google

        # Call the auth_callback function
        try:
            response = await auth_callback(
                provider="google",
                request=mock_request,
                response=MagicMock(),  # Using a mock response object
                db_session=mock_db_session
            )

            # Check if the response is a RedirectResponse and has the auth_token cookie
            if isinstance(response, RedirectResponse):
                print("✓ Callback returned a RedirectResponse")

                # Check if cookies were set properly
                cookies = response.headers.get_list('set-cookie')
                auth_cookies = [cookie for cookie in cookies if 'auth_token=' in cookie]

                if auth_cookies:
                    print("✓ Auth token cookie found in redirect response")
                    print(f"Cookies set: {len(cookies)}")
                    for cookie in cookies:
                        if 'auth_token' in cookie:
                            print(f"  - Auth cookie: {cookie.split(';')[0]}...")
                    return True
                else:
                    print("✗ No auth_token cookie found in redirect response")
                    print(f"All cookies: {cookies}")
                    return False
            else:
                print(f"✗ Expected RedirectResponse, got {type(response)}")
                return False

        except Exception as e:
            print(f"✗ Error during test: {e}")
            return False

def main():
    print("Running OAuth cookie fix test...")
    print("=" * 50)

    result = asyncio.run(test_oauth_callback_sets_cookie())

    print("=" * 50)
    if result:
        print("✓ Test PASSED: OAuth callback properly sets auth cookie")
    else:
        print("✗ Test FAILED: OAuth callback does not properly set auth cookie")

    return result

if __name__ == "__main__":
    main()