/**
 * Client-side authentication utilities
 *
 * This module provides client-safe authentication functions
 * that can be used in browser context.
 */
import { setAuthToken, clearAuthToken } from "./api";

const API_URL = typeof window !== "undefined"
  ? (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000")
  : "";

export interface User {
  id: string;
  email: string;
  name: string;
}

export interface Session {
  user: User;
  token: string;
}

/**
 * Sign in with email and password (client-side)
 */
export async function signIn(email: string, password: string): Promise<Session | null> {
  try {
    const response = await fetch(`${API_URL}/api/auth/sign-in`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
      credentials: "include",
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({ detail: "Sign in failed" }));
      throw new Error(data.detail || "Sign in failed");
    }

    const data = await response.json();

    // Store token in session storage for API requests
    if (data.token) {
      setAuthToken(data.token);
    }

    return data;
  } catch (error) {
    console.error("Sign in error:", error);
    return null;
  }
}

/**
 * Sign up with email and password (client-side)
 */
export async function signUp(
  email: string,
  password: string,
  name: string
): Promise<Session | null> {
  try {
    const response = await fetch(`${API_URL}/api/auth/sign-up`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, name }),
      credentials: "include",
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({ detail: "Sign up failed" }));
      throw new Error(data.detail || "Sign up failed");
    }

    const data = await response.json();

    // Store token in session storage for API requests
    if (data.token) {
      setAuthToken(data.token);
    }

    return data;
  } catch (error) {
    console.error("Sign up error:", error);
    return null;
  }
}

/**
 * Sign out - clears the session cookie (client-side)
 */
export async function signOut(): Promise<void> {
  try {
    await fetch(`${API_URL}/api/auth/sign-out`, {
      method: "POST",
      credentials: "include",
    });

    // Clear token from session storage
    clearAuthToken();
  } catch {
    // Clear token anyway
    clearAuthToken();
  }
}

/**
 * Get current session by fetching from the backend (client-side)
 */
export async function getSession(): Promise<Session | null> {
  try {
    const response = await fetch(`${API_URL}/api/auth/session`, {
      credentials: "include",
    });

    if (!response.ok) {
      return null;
    }

    const data = await response.json();
    return data;
  } catch {
    return null;
  }
}

/**
 * Get JWT token from localStorage or cookies (client-side)
 * Note: Token is set as HTTP-only cookie by the backend
 * This function fetches it via the session endpoint
 */
export async function getToken(): Promise<string | null> {
  const session = await getSession();
  return session?.token || null;
}

/**
 * Get current user from session (client-side)
 */
export async function getCurrentUser(): Promise<User | null> {
  const session = await getSession();
  return session?.user || null;
}
