"use client";

import { useState } from "react";

interface TaskItemProps {
  task: {
    id: number;
    user_id: string;
    title: string;
    description: string | null;
    completed: boolean;
    created_at: string;
    updated_at: string;
  };
  onTaskUpdated: () => void;
  onEditClick: (task: TaskItemProps["task"]) => void;
}

export function TaskItem({ task, onTaskUpdated, onEditClick }: TaskItemProps) {
  const [isLoading, setIsLoading] = useState(false);

  async function toggleComplete() {
    setIsLoading(true);
    try {
      const token = await getToken();
      if (!token) return;

      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${baseUrl}/api/tasks/${task.id}/complete`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        onTaskUpdated();
      }
    } finally {
      setIsLoading(false);
    }
  }

  async function deleteTask() {
    if (!confirm("Are you sure you want to delete this task?")) return;

    setIsLoading(true);
    try {
      const token = await getToken();
      if (!token) return;

      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${baseUrl}/api/tasks/${task.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        onTaskUpdated();
      }
    } finally {
      setIsLoading(false);
    }
  }

  async function getToken(): Promise<string | null> {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/auth/session`, {
        credentials: "include",
      });
      if (response.ok) {
        const data = await response.json();
        return data.token || null;
      }
      return null;
    } catch {
      return null;
    }
  }

  const formattedDate = new Date(task.created_at).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-4 transition-all ${task.completed ? "border-gray-200 bg-gray-50" : "border-gray-200"}`}>
      <div className="flex items-start gap-4">
        <button
          onClick={toggleComplete}
          disabled={isLoading}
          className={`mt-1 flex-shrink-0 w-5 h-5 rounded border-2 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors ${
            task.completed
              ? "bg-green-500 border-green-500 text-white"
              : "border-gray-300 hover:border-gray-400"
          }`}
        >
          {task.completed && (
            <svg className="w-full h-full p-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          )}
        </button>

        <div className="flex-1 min-w-0">
          <h3 className={`text-lg font-medium ${task.completed ? "text-gray-500 line-through" : "text-gray-900"}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`mt-1 text-sm ${task.completed ? "text-gray-400" : "text-gray-600"}`}>
              {task.description}
            </p>
          )}
          <p className="mt-2 text-xs text-gray-400">Created: {formattedDate}</p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => onEditClick(task)}
            disabled={isLoading}
            className="px-3 py-1 text-sm font-medium text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors"
          >
            Edit
          </button>
          <button
            onClick={deleteTask}
            disabled={isLoading}
            className="px-3 py-1 text-sm font-medium text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
