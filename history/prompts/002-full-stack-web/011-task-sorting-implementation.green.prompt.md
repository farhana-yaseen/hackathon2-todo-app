---
id: 11
title: Implement Task Sorting by Created and Due Date
stage: green
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-full-stack-web
branch: 002-full-stack-web
user: n/a
command: n/a
labels: [frontend, sorting, ux, usability, nextjs]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - phase-II/frontend/app/page.tsx
tests:
  - n/a
---

## Prompt

“Add sorting by due date and creation time”

## Response snapshot

Implemented flexible client-side sorting for the task list:
1. Added `sortBy` state in `phase-II/frontend/app/page.tsx`.
2. Created a dropdown selector (Newest First vs. Due Date) next to the status filters.
3. Implemented a sorting algorithm that handles null due dates (placing them at the end) and prioritizes logical sequence.
4. Ensured sorting works in conjunction with both the search bar and status filters.

## Outcome

- ✅ Impact: Users can now prioritize tasks based on their deadlines or see the most recently added ones first.
- 🧪 Tests: n/a
- 📁 Files: Modified 1 file.
- 🔁 Next prompts: Add ascending/descending toggle for sorting.
- 🧠 Reflection: Client-side sorting provides a responsive UX without requiring additional backend complexity for this scale of data.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): Add a visual indicator in TaskItem to show if it's currently sorted by due date.
