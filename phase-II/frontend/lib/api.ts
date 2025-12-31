/**
 * API Client for communicating with the FastAPI backend
 *
 * This module provides a type-safe API client that automatically
 * includes the JWT token from Better Auth for authentication.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Task interface matching the backend Task model
 */
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  due_date: string | null;
  reminder_enabled: boolean;
  category: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * Response types
 */
export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

export interface SuccessResponse {
  success: boolean;
  message: string;
}

export interface CategoryStat {
  category: string;
  count: number;
}

export interface StatsResponse {
  total_tasks: number;
  completed_tasks: number;
  active_tasks: number;
  overdue_tasks: number;
  category_stats: CategoryStat[];
}

/**
 * Get the JWT token from Better Auth session
 */
async function getAuthToken(): Promise<string | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/session`, {
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

/**
 * API client with JWT authentication
 */
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  /**
   * Make an authenticated request to the API
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await getAuthToken();

    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (token) {
      (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
      credentials: "include",
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Unknown error" }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // ========== Task Endpoints ==========

  /**
   * Get task statistics for the current user
   */
  async getTaskStats(): Promise<StatsResponse> {
    return this.request<StatsResponse>("/api/tasks/stats");
  }

  /**
   * Get all tasks for the current user
   */
  async getTasks(): Promise<TaskListResponse> {
    return this.request<TaskListResponse>("/api/tasks");
  }

  /**
   * Get a specific task by ID
   */
  async getTask(id: number): Promise<Task> {
    return this.request<Task>(`/api/tasks/${id}`);
  }

  /**
   * Create a new task
   */
  async createTask(data: {
    title: string;
    description?: string;
    due_date?: string | null;
    reminder_enabled?: boolean;
    category?: string | null;
  }): Promise<Task> {
    return this.request<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  /**
   * Update an existing task
   */
  async updateTask(
    id: number,
    data: {
      title?: string;
      description?: string;
      due_date?: string | null;
      reminder_enabled?: boolean;
      category?: string | null;
    }
  ): Promise<Task> {
    return this.request<Task>(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  /**
   * Toggle task completion status
   */
  async toggleComplete(id: number): Promise<Task> {
    return this.request<Task>(`/api/tasks/${id}/complete`, {
      method: "PATCH",
    });
  }

  /**
   * Delete a task
   */
  async deleteTask(id: number): Promise<SuccessResponse> {
    return this.request<SuccessResponse>(`/api/tasks/${id}`, {
      method: "DELETE",
    });
  }
}

/**
 * Export a singleton API client instance
 */
export const api = new ApiClient(API_BASE_URL);

/**
 * Export the API client class for custom instances
 */
export { ApiClient };
