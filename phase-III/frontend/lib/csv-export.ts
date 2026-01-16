/**
 * CSV Export Utility
 *
 * Provides functions to export tasks to CSV format
 */

import { Task } from "./api";
import format from "date-fns/format";
import parseISO from "date-fns/parseISO";

/**
 * Convert tasks array to CSV string
 */
export function tasksToCSV(tasks: Task[]): string {
  // Define CSV headers
  const headers = [
    "ID",
    "Title",
    "Description",
    "Category",
    "Status",
    "Due Date",
    "Reminder Enabled",
    "Created At",
    "Updated At"
  ];

  // Create CSV header row
  const headerRow = headers.join(",");

  // Create CSV data rows
  const dataRows = tasks.map(task => {
    return [
      task.id,
      escapeCSVField(task.title),
      escapeCSVField(task.description || ""),
      escapeCSVField(task.category || ""),
      task.completed ? "Completed" : "Active",
      task.due_date ? format(parseISO(task.due_date), "yyyy-MM-dd HH:mm:ss") : "",
      task.reminder_enabled ? "Yes" : "No",
      format(parseISO(task.created_at), "yyyy-MM-dd HH:mm:ss"),
      format(parseISO(task.updated_at), "yyyy-MM-dd HH:mm:ss")
    ].join(",");
  });

  // Combine header and data rows
  return [headerRow, ...dataRows].join("\n");
}

/**
 * Escape CSV field (handle commas, quotes, and newlines)
 */
function escapeCSVField(field: string): string {
  // If field contains comma, quote, or newline, wrap in quotes and escape existing quotes
  if (field.includes(",") || field.includes('"') || field.includes("\n")) {
    return `"${field.replace(/"/g, '""')}"`;
  }
  return field;
}

/**
 * Download CSV file
 */
export function downloadCSV(csvContent: string, filename: string = "tasks.csv"): void {
  // Create blob from CSV content
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

  // Create download link
  const link = document.createElement("a");
  const url = URL.createObjectURL(blob);

  link.setAttribute("href", url);
  link.setAttribute("download", filename);
  link.style.visibility = "hidden";

  // Trigger download
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  // Clean up
  URL.revokeObjectURL(url);
}

/**
 * Export tasks to CSV and trigger download
 */
export function exportTasksToCSV(tasks: Task[], filename?: string): void {
  const csvContent = tasksToCSV(tasks);
  const timestamp = format(new Date(), "yyyy-MM-dd-HHmmss");
  const defaultFilename = `tasks-export-${timestamp}.csv`;
  downloadCSV(csvContent, filename || defaultFilename);
}
