"use client";

import { useEffect, useState } from "react";
import { signOut, getCurrentUser, getCurrentUser as getUserFromClient } from "@/lib/auth-client";

interface User {
  id: string;
  email: string;
  name: string;
}

export function Navbar() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function checkSession() {
      try {
        const currentUser = await getUserFromClient();
        if (currentUser) {
          setUser({
            id: currentUser.id,
            email: currentUser.email || "",
            name: currentUser.name || "",
          });
        } else {
          setUser(null);
        }
      } finally {
        setIsLoading(false);
      }
    }
    checkSession();
  }, []);

  async function handleSignOut() {
    await signOut();
    setUser(null);
  }

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-900">Todo App</h1>
          </div>
          <div className="flex items-center gap-4">
            {isLoading ? (
              <span className="text-gray-500">Loading...</span>
            ) : user ? (
              <>
                <span className="text-sm text-gray-600">
                  {user.name} ({user.email})
                </span>
                <button
                  onClick={handleSignOut}
                  className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                  Sign Out
                </button>
              </>
            ) : null}
          </div>
        </div>
      </div>
    </nav>
  );
}
