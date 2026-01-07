"use client";

import { useEffect, useState } from "react";
import { Navbar } from "@/components/Navbar";
import { TaskForm } from "@/components/TaskForm";
import { TaskList } from "@/components/TaskList";
import { CalendarView } from "@/components/CalendarView";
import { DashboardStats } from "@/components/DashboardStats";
import { api, Task, StatsResponse } from "@/lib/api";
import { getCurrentUser } from "@/lib/auth-client";
import { exportTasksToCSV } from "@/lib/csv-export";

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<any>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filter, setFilter] = useState<"all" | "active" | "completed">("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState<"created" | "due">("created");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [isStatsLoading, setIsStatsLoading] = useState(true);
  const [view, setView] = useState<"list" | "calendar">("list");

  // Extract token from URL and store it when component mounts
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');

    if (token && typeof window !== 'undefined') {
      // Store token in sessionStorage for API calls
      sessionStorage.setItem('auth_token', token);

      // Remove token from URL to prevent it from being visible in address bar
      const newUrl = window.location.pathname + window.location.hash;
      window.history.replaceState({}, document.title, newUrl);
    }
  }, []);

  const categories = ["Work", "Personal", "Shopping", "Health", "Education", "Other"];

  async function fetchTasks() {
    try {
      const tasksResponse = await api.getTasks();
      setTasks(tasksResponse.tasks);

      setIsStatsLoading(true);
      const statsResponse = await api.getTaskStats();
      setStats(statsResponse);
    } catch (error) {
      console.error("Failed to fetch tasks or stats:", error);
    } finally {
      setIsLoading(false);
      setIsStatsLoading(false);
    }
  }

  const filteredTasks = tasks
    .filter((task) => {
      const matchesFilter =
        filter === "active" ? !task.completed :
        filter === "completed" ? task.completed :
        true;

      const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesCategory =
        selectedCategory === "all" || task.category === selectedCategory;

      return matchesFilter && matchesSearch && matchesCategory;
    })
    .sort((a, b) => {
      if (sortBy === "due") {
        if (!a.due_date) return 1;
        if (!b.due_date) return -1;
        return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
      }
      // Default: sort by creation time (newest first)
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    });

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

    // Listen for auth state changes (e.g., sign out from other components)
    const handleAuthChange = async () => {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
      if (currentUser) {
        await fetchTasks();
      } else {
        setIsLoading(false);
      }
    };

    window.addEventListener("authStateChanged", handleAuthChange);

    // Clean up event listener on unmount
    return () => {
      window.removeEventListener("authStateChanged", handleAuthChange);
    };
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
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
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
            <DashboardStats stats={stats} isLoading={isStatsLoading} />

            <div className="space-y-6 mb-8">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Your Tasks</h2>
                  <div className="flex bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
                    <button
                      onClick={() => setView("list")}
                      className={`px-3 py-1 text-sm font-medium rounded-md transition-colors flex items-center gap-1 cursor-pointer ${
                        view === "list" ? "bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-sm" : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                      }`}
                    >
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                      </svg>
                      List
                    </button>
                    <button
                      onClick={() => setView("calendar")}
                      className={`px-3 py-1 text-sm font-medium rounded-md transition-colors flex items-center gap-1 cursor-pointer ${
                        view === "calendar" ? "bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-sm" : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                      }`}
                    >
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      Calendar
                    </button>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  <div className="flex bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
                    <button
                      onClick={() => setFilter("all")}
                      className={`px-3 py-1 text-sm font-medium rounded-md transition-colors cursor-pointer ${
                        filter === "all" ? "bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-sm" : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                      }`}
                    >
                      All
                    </button>
                    <button
                      onClick={() => setFilter("active")}
                      className={`px-3 py-1 text-sm font-medium rounded-md transition-colors cursor-pointer ${
                        filter === "active" ? "bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-sm" : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                      }`}
                    >
                      Active
                    </button>
                    <button
                      onClick={() => setFilter("completed")}
                      className={`px-3 py-1 text-sm font-medium rounded-md transition-colors cursor-pointer ${
                        filter === "completed" ? "bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-sm" : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                      }`}
                    >
                      Completed
                    </button>
                  </div>

                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as "created" | "due")}
                    className="block w-full sm:w-auto pl-3 pr-10 py-1 text-sm border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-lg bg-gray-100 dark:bg-gray-800 border-none font-medium text-gray-700 dark:text-gray-200"
                  >
                    <option value="created">Newest First</option>
                    <option value="due">Due Date</option>
                  </select>

                  <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    className="block w-full sm:w-auto pl-3 pr-10 py-1 text-sm border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-lg bg-gray-100 dark:bg-gray-800 border-none font-medium text-gray-700 dark:text-gray-200"
                  >
                    <option value="all">All Categories</option>
                    {categories.map((cat) => (
                      <option key={cat} value={cat}>
                        {cat}
                      </option>
                    ))}
                  </select>

                  <button
                    onClick={() => exportTasksToCSV(filteredTasks)}
                    disabled={filteredTasks.length === 0}
                    className="px-3 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2 cursor-pointer"
                    title="Export tasks to CSV"
                  >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Export CSV
                  </button>
                </div>
              </div>

              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input
                  type="text"
                  placeholder="Search tasks by title..."
                  className="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-700 rounded-xl leading-5 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </div>

            {view === "list" ? (
              <TaskList
                tasks={filteredTasks}
                onTaskUpdated={fetchTasks}
                onEditClick={(task) => setEditingTask(task)}
              />
            ) : (
              <CalendarView
                tasks={filteredTasks}
                onTaskUpdated={fetchTasks}
                onEditClick={(task) => setEditingTask(task)}
              />
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
