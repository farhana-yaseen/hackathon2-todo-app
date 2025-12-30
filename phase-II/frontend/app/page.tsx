"use client";

import { useEffect, useState } from "react";
import { Navbar } from "@/components/Navbar";
import { TaskForm } from "@/components/TaskForm";
import { TaskList } from "@/components/TaskList";
import { api, Task } from "@/lib/api";
import { getCurrentUser } from "@/lib/auth-client";

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<any>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  async function fetchTasks() {
    try {
      const response = await api.getTasks();
      setTasks(response.tasks);
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    async function init() {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
      if (currentUser) {
        await fetchTasks();
      } else {
        setIsLoading(false);
      }
    }
    init();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4">
        <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Todo App</h1>
          <p className="text-gray-600 mb-8">Please sign in to manage your tasks.</p>
          <div className="space-y-4">
            <a
              href="/auth/sign-in"
              className="block w-full py-3 px-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
            >
              Sign In
            </a>
            <a
              href="/auth/sign-up"
              className="block w-full py-3 px-4 bg-white text-blue-600 font-semibold border-2 border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
            >
              Create Account
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-1">
            <TaskForm
              onTaskCreated={() => {
                fetchTasks();
                setEditingTask(null);
              }}
              editingTask={editingTask}
              onCancelEdit={() => setEditingTask(null)}
            />
          </div>
          <div className="md:col-span-2">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Your Tasks</h2>
            <TaskList
              tasks={tasks}
              onTaskUpdated={fetchTasks}
              onEditClick={(task) => setEditingTask(task)}
            />
          </div>
        </div>
      </div>
    </main>
  );
}
