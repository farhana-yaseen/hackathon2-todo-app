"use client";

import { useEffect, useState } from "react";
import { signOut, getCurrentUser as getUserFromClient, getToken } from "@/lib/auth-client";
import { checkNotificationSupport, subscribeToPush, unsubscribeFromPush } from "@/lib/push";

interface User {
  id: string;
  email: string;
  name: string;
}

export function Navbar() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isNotificationsEnabled, setIsNotificationsEnabled] = useState(false);
  const [isPushSupported, setIsPushSupported] = useState(false);

  useEffect(() => {
    async function init() {
      try {
        const currentUser = await getUserFromClient();
        if (currentUser) {
          setUser({
            id: currentUser.id,
            email: currentUser.email || "",
            name: currentUser.name || "",
          });

          // Check notification support
          const { supported, permission } = await checkNotificationSupport();
          setIsPushSupported(supported);
          setIsNotificationsEnabled(permission === "granted");
        } else {
          setUser(null);
        }
      } finally {
        setIsLoading(false);
      }
    }
    init();
  }, []);

  async function toggleNotifications() {
    const token = await getToken();
    if (!token) return;

    try {
      if (isNotificationsEnabled) {
        await unsubscribeFromPush(token);
        setIsNotificationsEnabled(false);
      } else {
        await subscribeToPush(token);
        setIsNotificationsEnabled(true);
      }
    } catch (error) {
      console.error("Failed to toggle notifications:", error);
      alert("Failed to enable notifications. Please check browser permissions.");
    }
  }

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
                {isPushSupported && (
                  <button
                    onClick={toggleNotifications}
                    title={isNotificationsEnabled ? "Notifications enabled" : "Enable notifications"}
                    className={`p-2 rounded-full transition-colors ${
                      isNotificationsEnabled ? "text-blue-600 bg-blue-50" : "text-gray-400 hover:text-gray-600 hover:bg-gray-100"
                    }`}
                  >
                    <svg className="w-5 h-5" fill={isNotificationsEnabled ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                    </svg>
                  </button>
                )}
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
