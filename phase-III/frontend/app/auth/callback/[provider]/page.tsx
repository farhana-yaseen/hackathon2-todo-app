"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { api, setAuthToken } from "@/lib/api";

export default function OAuthCallback() {
  const router = useRouter();

  useEffect(() => {
    // Call the session endpoint to get the token after successful OAuth
    const fetchSession = async () => {
      try {
        // Wait a moment to ensure the cookie is set by the redirect
        await new Promise(resolve => setTimeout(resolve, 500));

        // Explicitly call the session endpoint to get the token
        const sessionResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/auth/session`, {
          credentials: 'include'
        });

        if (sessionResponse.ok) {
          const sessionData = await sessionResponse.json();
          const token = sessionData.token;

          if (token) {
            // Store the token in sessionStorage for API calls
            if (typeof window !== 'undefined') {
              sessionStorage.setItem('auth_token', token);
              setAuthToken(token); // This will also store it in sessionStorage
            }

            // Dispatch a custom event to notify other components about the auth state change
            window.dispatchEvent(new Event('storage'));

            // Redirect to home page
            router.push('/');
            router.refresh();
          } else {
            // If no token, redirect to sign-in with error
            router.push('/auth/sign-in?error=Authentication failed');
          }
        } else {
          // If session fetch fails, redirect to sign-in with error
          router.push('/auth/sign-in?error=Authentication failed');
        }
      } catch (error) {
        console.error('OAuth session fetch failed:', error);
        // If session fetch fails, redirect to sign-in with error
        router.push('/auth/sign-in?error=Authentication failed');
      }
    };

    fetchSession();
  }, [router]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
        <div className="flex justify-center mb-4">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
        </div>
        <h2 className="text-xl font-semibold text-center text-gray-800">Completing authentication...</h2>
        <p className="text-center text-gray-600 mt-2">Please wait while we complete the login process.</p>
      </div>
    </div>
  );
}