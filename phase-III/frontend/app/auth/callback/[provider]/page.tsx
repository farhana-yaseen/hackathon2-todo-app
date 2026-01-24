"use client";

import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useSession } from "@/contexts/SessionProvider";

export default function OAuthCallback() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { refresh } = useSession();

  useEffect(() => {
    const token = searchParams.get('token');

    if (token) {
      // Store the token in sessionStorage for API calls
      if (typeof window !== 'undefined') {
        sessionStorage.setItem('auth_token', token);
      }

      // Refresh the session to update the UI
      refresh();

      // Redirect to home page
      router.push('/');
      router.refresh();
    } else {
      // If no token, redirect to sign-in with error
      router.push('/auth/sign-in?error=Authentication failed');
    }
  }, [searchParams, router, refresh]);

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