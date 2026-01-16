"use client";

import { StatsResponse } from "@/lib/api";

interface DashboardStatsProps {
  stats: StatsResponse | null;
  isLoading: boolean;
}

export function DashboardStats({ stats, isLoading }: DashboardStatsProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 animate-pulse">
            <div className="h-4 w-16 bg-gray-100 rounded mb-2"></div>
            <div className="h-8 w-8 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  if (!stats) return null;

  const statCards = [
    {
      label: "Total Tasks",
      value: stats.total_tasks,
      color: "text-blue-600",
      bg: "bg-blue-50",
    },
    {
      label: "Active",
      value: stats.active_tasks,
      color: "text-yellow-600",
      bg: "bg-yellow-50",
    },
    {
      label: "Completed",
      value: stats.completed_tasks,
      color: "text-green-600",
      bg: "bg-green-50",
    },
    {
      label: "Overdue",
      value: stats.overdue_tasks,
      color: "text-red-600",
      bg: "bg-red-50",
    },
  ];

  return (
    <div className="space-y-6 mb-8">
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card) => (
          <div
            key={card.label}
            className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-col"
          >
            <span className="text-sm font-medium text-gray-500">{card.label}</span>
            <span className={`text-2xl font-bold mt-1 ${card.color}`}>{card.value}</span>
          </div>
        ))}
      </div>

      {stats.category_stats.length > 0 && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-sm font-semibold text-gray-900 mb-4 uppercase tracking-wider">
            Tasks by Category
          </h3>
          <div className="space-y-4">
            {stats.category_stats.map((cat) => {
              const percentage = stats.total_tasks > 0
                ? (cat.count / stats.total_tasks) * 100
                : 0;

              return (
                <div key={cat.category} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium text-gray-700">{cat.category}</span>
                    <span className="text-gray-500">{cat.count}</span>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
