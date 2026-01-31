'use client';

import { useEffect, useRef } from 'react';
import { getCurrentUser } from '@/lib/auth-client';

interface TaskWebSocketClientProps {
  onTaskUpdate: () => void;
}

export function TaskWebSocketClient({ onTaskUpdate }: TaskWebSocketClientProps) {
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let reconnectTimeout: NodeJS.Timeout | null = null;

    const connectWebSocket = async () => {
      try {
        const user = await getCurrentUser();
        if (!user?.id) {
          console.warn('User not authenticated, skipping WebSocket connection');
          return;
        }

        // Close any existing connection
        if (wsRef.current) {
          wsRef.current.close();
        }

        // Get the WebSocket URL based on environment
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/${user.id}`;

        console.log(`Connecting to WebSocket: ${wsUrl}`);

        wsRef.current = new WebSocket(wsUrl);

        wsRef.current.onopen = () => {
          console.log('WebSocket connected');
          if (reconnectTimeout) {
            clearTimeout(reconnectTimeout);
            reconnectTimeout = null;
          }
        };

        wsRef.current.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data);

            // Check if it's a task update message
            if (message.event === 'task_update') {
              console.log('Received task update:', message);
              // Trigger the callback to refresh tasks
              onTaskUpdate();
            }
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        wsRef.current.onclose = (event) => {
          console.log('WebSocket closed:', event.code, event.reason);

          // Attempt to reconnect after a delay (exponential backoff)
          if (reconnectTimeout) {
            clearTimeout(reconnectTimeout);
          }
          reconnectTimeout = setTimeout(connectWebSocket, 3000); // Retry after 3 seconds
        };

        wsRef.current.onerror = (error) => {
          console.error('WebSocket error:', error);
        };
      } catch (error) {
        console.error('Error connecting to WebSocket:', error);

        // Retry after a delay
        if (reconnectTimeout) {
          clearTimeout(reconnectTimeout);
        }
        reconnectTimeout = setTimeout(connectWebSocket, 3000);
      }
    };

    // Connect to WebSocket
    connectWebSocket();

    // Cleanup function
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
      }
    };
  }, [onTaskUpdate]);

  return null; // This component doesn't render anything
}