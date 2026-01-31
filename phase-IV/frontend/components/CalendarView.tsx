"use client";

import { useMemo, useState } from "react";
import format from "date-fns/format";
import startOfMonth from "date-fns/startOfMonth";
import endOfMonth from "date-fns/endOfMonth";
import startOfWeek from "date-fns/startOfWeek";
import endOfWeek from "date-fns/endOfWeek";
import eachDayOfInterval from "date-fns/eachDayOfInterval";
import isSameMonth from "date-fns/isSameMonth";
import isSameDay from "date-fns/isSameDay";
import addMonths from "date-fns/addMonths";
import subMonths from "date-fns/subMonths";
import parseISO from "date-fns/parseISO";
import isPast from "date-fns/isPast";
import isToday from "date-fns/isToday";
import isWithinInterval from "date-fns/isWithinInterval";
import startOfDay from "date-fns/startOfDay";
import endOfDay from "date-fns/endOfDay";
import { Task } from "@/lib/api";
import { exportTasksToCSV } from "@/lib/csv-export";

interface CalendarViewProps {
  tasks: Task[];
  onTaskUpdated: () => void;
  onEditClick: (task: Task) => void;
}

export function CalendarView({ tasks, onTaskUpdated, onEditClick }: CalendarViewProps) {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [dateRangeFilter, setDateRangeFilter] = useState<{
    start: string | null;
    end: string | null;
  }>({ start: null, end: null });
  const [showDateRangePicker, setShowDateRangePicker] = useState(false);

  // Generate calendar days
  const days = useMemo(() => {
    const start = startOfWeek(startOfMonth(currentMonth));
    const end = endOfWeek(endOfMonth(currentMonth));
    return eachDayOfInterval({ start, end });
  }, [currentMonth]);

  // Filter tasks that have a due date and apply date range filter
  const tasksWithDates = useMemo(() => {
    let filtered = tasks.filter(task => task.due_date);

    // Apply date range filter if set
    if (dateRangeFilter.start && dateRangeFilter.end) {
      const rangeStart = startOfDay(parseISO(dateRangeFilter.start));
      const rangeEnd = endOfDay(parseISO(dateRangeFilter.end));

      filtered = filtered.filter(task => {
        const taskDate = parseISO(task.due_date!);
        return isWithinInterval(taskDate, { start: rangeStart, end: rangeEnd });
      });
    }

    return filtered;
  }, [tasks, dateRangeFilter]);

  const getTasksForDay = (day: Date) => {
    return tasksWithDates.filter(task => isSameDay(parseISO(task.due_date!), day));
  };

  const clearDateRange = () => {
    setDateRangeFilter({ start: null, end: null });
    setShowDateRangePicker(false);
  };

  const applyDateRange = () => {
    setShowDateRangePicker(false);
  };

  const isDateRangeActive = dateRangeFilter.start !== null && dateRangeFilter.end !== null;

  const nextMonth = () => setCurrentMonth(addMonths(currentMonth, 1));
  const prevMonth = () => setCurrentMonth(subMonths(currentMonth, 1));

  const categoryColors: Record<string, string> = {
    Work: "bg-blue-100 text-blue-800 border-blue-200",
    Personal: "bg-green-100 text-green-800 border-green-200",
    Shopping: "bg-purple-100 text-purple-800 border-purple-200",
    Health: "bg-red-100 text-red-800 border-red-200",
    Education: "bg-yellow-100 text-yellow-800 border-yellow-200",
    Other: "bg-gray-100 text-gray-800 border-gray-200",
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Calendar Header */}
      <div className="px-6 py-4 border-b border-gray-200 space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">
            {format(currentMonth, "MMMM yyyy")}
          </h2>
          <div className="flex gap-2">
            <button
              onClick={() => exportTasksToCSV(tasksWithDates)}
              disabled={tasksWithDates.length === 0}
              className="px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2 cursor-pointer"
              title="Export visible tasks to CSV"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Export
            </button>
            <button
              onClick={() => setShowDateRangePicker(!showDateRangePicker)}
              className={`px-3 py-1.5 text-sm font-medium rounded-lg transition-colors flex items-center gap-2 cursor-pointer ${
                isDateRangeActive
                  ? "bg-blue-600 text-white hover:bg-blue-700"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
              title="Filter by date range"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              {isDateRangeActive ? "Filtered" : "Filter"}
            </button>
            <button
              onClick={prevMonth}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors cursor-pointer"
              title="Previous month"
            >
              <svg className="w-5 h-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
              onClick={nextMonth}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors cursor-pointer"
              title="Next month"
            >
              <svg className="w-5 h-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>

        {/* Date Range Picker */}
        {showDateRangePicker && (
          <div className="bg-gray-50 rounded-lg p-4 space-y-3">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Start Date
                </label>
                <input
                  type="date"
                  value={dateRangeFilter.start || ""}
                  onChange={(e) => setDateRangeFilter(prev => ({ ...prev, start: e.target.value }))}
                  className="block w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  End Date
                </label>
                <input
                  type="date"
                  value={dateRangeFilter.end || ""}
                  onChange={(e) => setDateRangeFilter(prev => ({ ...prev, end: e.target.value }))}
                  className="block w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={applyDateRange}
                disabled={!dateRangeFilter.start || !dateRangeFilter.end}
                className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors cursor-pointer"
              >
                Apply Filter
              </button>
              {isDateRangeActive && (
                <button
                  onClick={clearDateRange}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
                >
                  Clear
                </button>
              )}
            </div>
            {isDateRangeActive && (
              <div className="text-xs text-gray-600 bg-blue-50 px-3 py-2 rounded">
                Showing tasks from <span className="font-semibold">{format(parseISO(dateRangeFilter.start!), "MMM d, yyyy")}</span> to <span className="font-semibold">{format(parseISO(dateRangeFilter.end!), "MMM d, yyyy")}</span>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Days Header */}
      <div className="grid grid-cols-7 border-b border-gray-200 bg-gray-50">
        {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
          <div key={day} className="py-2 text-center text-xs font-semibold text-gray-500 uppercase tracking-wider">
            {day}
          </div>
        ))}
      </div>

      {/* Calendar Grid */}
      <div className="grid grid-cols-7 grid-rows-5 md:grid-rows-6">
        {days.map((day: Date, idx: number) => {
          const dayTasks = getTasksForDay(day);
          const isCurrentMonth = isSameMonth(day, currentMonth);
          const isTodayDate = isToday(day);

          return (
            <div
              key={day.toISOString()}
              className={`min-h-[100px] p-2 border-r border-b border-gray-100 last:border-r-0 ${
                !isCurrentMonth ? "bg-gray-50 text-gray-400" : "text-gray-900"
              }`}
            >
              <div className="flex justify-between items-center mb-1">
                <span className={`text-sm font-medium w-7 h-7 flex items-center justify-center rounded-full ${
                  isTodayDate ? "bg-blue-600 text-white" : ""
                }`}>
                  {format(day, "d")}
                </span>
              </div>
              <div className="space-y-1">
                {dayTasks.map((task) => (
                  <button
                    key={task.id}
                    onClick={() => onEditClick(task)}
                    className={`w-full text-left px-2 py-1 text-[10px] leading-tight rounded border border-transparent truncate hover:shadow-sm transition-all cursor-pointer ${
                      task.completed
                        ? "bg-gray-100 text-gray-400 line-through"
                        : (categoryColors[task.category || "Other"] || categoryColors.Other)
                    } ${!task.completed && isPast(parseISO(task.due_date!)) && !isToday(parseISO(task.due_date!)) ? "ring-1 ring-red-400" : ""}`}
                    title={`${task.title}${task.completed ? " (Completed)" : ""}`}
                  >
                    {task.title}
                  </button>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer / Legend */}
      <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 flex flex-wrap gap-4 text-[10px] text-gray-500 font-medium">
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full border border-red-400 ring-1 ring-red-400 ring-offset-1"></div>
          <span>Overdue</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-gray-200"></div>
          <span>Completed</span>
        </div>
        {Object.entries(categoryColors).map(([cat, colorClass]) => (
          <div key={cat} className="flex items-center gap-1.5">
            <div className={`w-2 h-2 rounded-full ${colorClass.split(" ")[0]}`}></div>
            <span>{cat}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
