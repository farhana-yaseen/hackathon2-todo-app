"use client";

import { useState } from "react";

interface TaskFormProps {
  onTaskCreated: () => void;
  editingTask?: {
    id: number;
    title: string;
    description: string | null;
    due_date?: string | null;
    reminder_enabled?: boolean;
    category?: string | null;
  } | null;
  onCancelEdit?: () => void;
}

export function TaskForm({ onTaskCreated, editingTask, onCancelEdit }: TaskFormProps) {
  const [title, setTitle] = useState(editingTask?.title || "");
  const [description, setDescription] = useState(editingTask?.description || "");
  const [dueDate, setDueDate] = useState(editingTask?.due_date ? editingTask.due_date.slice(0, 16) : "");
  const [reminderEnabled, setReminderEnabled] = useState(editingTask?.reminder_enabled || false);
  const [category, setCategory] = useState(editingTask?.category || "");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const categories = ["Work", "Personal", "Shopping", "Health", "Education", "Other"];

  const isEditing = !!editingTask;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const token = await getToken();
      if (!token) {
        throw new Error("Not authenticated");
      }

      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const url = isEditing
        ? `${baseUrl}/api/tasks/${editingTask.id}`
        : `${baseUrl}/api/tasks`;
      const method = isEditing ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title,
          description: description || undefined,
          due_date: dueDate ? new Date(dueDate).toISOString() : null,
          reminder_enabled: reminderEnabled,
          category: category || null,
        }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(data.detail || "Failed to save task");
      }

      setTitle("");
      setDescription("");
      setDueDate("");
      setReminderEnabled(false);
      setCategory("");
      onTaskCreated();
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
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

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-lg font-medium text-gray-900">
        {isEditing ? "Edit Task" : "Add New Task"}
      </h2>

      {error && (
        <div className="p-3 text-sm text-red-600 bg-red-50 rounded-md">{error}</div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          minLength={1}
          maxLength={200}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
          placeholder="Enter task title"
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description (optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={1000}
          rows={3}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
          placeholder="Enter task description"
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label htmlFor="due_date" className="block text-sm font-medium text-gray-700">
            Due Date (optional)
          </label>
          <input
            type="datetime-local"
            id="due_date"
            value={dueDate}
            onChange={(e) => {
              setDueDate(e.target.value);
              // Blur the input to help close the datetime picker after selection
              e.target.blur();
            }}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border cursor-pointer"
          />
        </div>

        <div className="flex items-center mt-6">
          <input
            type="checkbox"
            id="reminder_enabled"
            checked={reminderEnabled}
            onChange={(e) => setReminderEnabled(e.target.checked)}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label htmlFor="reminder_enabled" className="ml-2 block text-sm text-gray-900">
            Enable Reminder
          </label>
        </div>
      </div>

      <div>
        <label htmlFor="category" className="block text-sm font-medium text-gray-700">
          Category
        </label>
        <select
          id="category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
        >
          <option value="">No Category</option>
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      <div className="flex gap-3">
        <button
          type="submit"
          disabled={isLoading || !title.trim()}
          className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          {isLoading ? "Saving..." : isEditing ? "Update Task" : "Add Task"}
        </button>

        {isEditing && onCancelEdit && (
          <button
            type="button"
            onClick={onCancelEdit}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 cursor-pointer"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
  