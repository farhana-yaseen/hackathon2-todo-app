/**
 * Utility for managing Web Push notifications in the frontend.
 */

const VAPID_PUBLIC_KEY = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY;
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Converts a base64 string to a Uint8Array for the push manager.
 */
function urlBase64ToUint8Array(base64String: string) {
  const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/");

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

/**
 * Checks if push notifications are supported and permitted.
 */
export async function checkNotificationSupport() {
  if (!("serviceWorker" in navigator) || !("PushManager" in window)) {
    return { supported: false, permission: "denied" };
  }
  return { supported: true, permission: Notification.permission };
}

/**
 * Registers the service worker and subscribes the user to push notifications.
 */
export async function subscribeToPush(token: string) {
  if (!VAPID_PUBLIC_KEY) {
    console.error("VAPID public key not found in environment variables");
    return null;
  }

  try {
    // 1. Register Service Worker
    const registration = await navigator.serviceWorker.register("/sw.js", {
      scope: "/",
    });

    // 2. Request Permission
    const permission = await Notification.requestPermission();
    if (permission !== "granted") {
      throw new Error("Notification permission not granted");
    }

    // 3. Subscribe to Push Manager
    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
    });

    // 4. Send subscription to backend
    const response = await fetch(`${API_BASE_URL}/api/notifications/subscribe`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        endpoint: subscription.endpoint,
        keys: {
          p256dh: btoa(String.fromCharCode.apply(null, Array.from(new Uint8Array(subscription.getKey("p256dh")!)))),
          auth: btoa(String.fromCharCode.apply(null, Array.from(new Uint8Array(subscription.getKey("auth")!)))),
        },
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to sync subscription with backend");
    }

    return subscription;
  } catch (error) {
    console.error("Error subscribing to push:", error);
    throw error;
  }
}

/**
 * Unsubscribes the user from push notifications.
 */
export async function unsubscribeFromPush(token: string) {
  try {
    const registration = await navigator.serviceWorker.ready;
    const subscription = await registration.pushManager.getSubscription();

    if (subscription) {
      await subscription.unsubscribe();
      // Optional: Tell backend to remove subscription
    }
    return true;
  } catch (error) {
    console.error("Error unsubscribing from push:", error);
    return false;
  }
}
