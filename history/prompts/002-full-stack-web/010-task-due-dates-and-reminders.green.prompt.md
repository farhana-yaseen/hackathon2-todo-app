---
id: 10
title: Implement Task Due Dates and Reminders
stage: green
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-full-stack-web
branch: 002-full-stack-web
user: n/a
command: n/a
labels: [backend, frontend, database, ui, performance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - phase-II/backend/src/models/task.py
  - phase-II/backend/src/api/routes/tasks.py
  - phase-II/frontend/lib/api.ts
  - phase-II/frontend/components/TaskForm.tsx
  - phase-II/frontend/components/TaskItem.tsx
tests:
  - n/a
---

## Prompt

“Add task due dates and reminders”

## Response snapshot

Implemented comprehensive due date and reminder support across the full stack:
1. Updated `Task` SQLModel in the backend to include `due_date` (datetime) and `reminder_enabled` (boolean).
2. Enhanced backend API routes (`create_task`, `update_task`) and Pydantic models to handle the new fields.
3. Updated frontend `Task` interface and API client.
4. Added a datetime picker and reminder toggle to `TaskForm.tsx`.
5. Enhanced `TaskItem.tsx` to display due dates, show overdue status in red, and display a reminder icon.

## Outcome

- ✅ Impact: Users can now schedule tasks and track deadlines.
- 🧪 Tests: n/a
- 📁 Files: Modified 5 files across backend and frontend.
- 🔁 Next prompts: Implement actual email/push notification logic for reminders.
- 🧠 Reflection: Using standard `datetime-local` input and ISO strings ensures compatibility between browser and server environments.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): Add a "Sort by due date" option to the task list.
