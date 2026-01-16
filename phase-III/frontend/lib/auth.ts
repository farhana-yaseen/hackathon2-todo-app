/**
 * Simple JWT Authentication for Next.js frontend
 *
 * This module handles authentication with the FastAPI backend
 * using JWT tokens. The backend issues JWT tokens via Better Auth.
 */
import { cookies } from "next/headers";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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
 * Sign in with email and password
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
    return data;
  } catch (error) {
    console.error("Sign in error:", error);
    return null;
  }
}

/**
 * Sign up with email and password
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
    return data;
  } catch (error) {
    console.error("Sign up error:", error);
    return null;
  }
}

/**
 * Sign out - clears the session cookie
 */
export async function signOut(): Promise<void> {
  try {
    await fetch(`${API_URL}/api/auth/sign-out`, {
      method: "POST",
      credentials: "include",
    });
  } catch {
    // Ignore errors
  }
}

/**
 * Get current session from cookies (server-side only)
 */
export async function getSession(): Promise<Session | null> {
  try {
    const cookieStore = await cookies();
    const token = cookieStore.get("auth_token")?.value;

    if (!token) {
      return null;
    }

    // Decode JWT to get user info
    const payload = decodeJWT(token);
    if (!payload) {
      return null;
    }

    return {
      user: {
        id: (payload.sub as string) || (payload.id as string) || "",
        email: (payload.email as string) || "",
        name: (payload.name as string) || "",
      },
      token,
    };
  } catch {
    return null;
  }
}

/**
 * Get JWT token from cookies (server-side only)
 */
export async function getToken(): Promise<string | null> {
  try {
    const cookieStore = await cookies();
    return cookieStore.get("auth_token")?.value || null;
  } catch {
    return null;
  }
}

/**
 * Get current user from session (server-side only)
 */
export async function getCurrentUser(): Promise<User | null> {
  const session = await getSession();
  return session?.user || null;
}

/**
 * Simple JWT decoder (for client-side use)
 */
function decodeJWT(token: string): Record<string, unknown> | null {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return null;

    const payload = parts[1];
    const decoded = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
    return JSON.parse(decoded);
  } catch {
    return null;
  }
}
