---
id: 1
title: "Create spec for Todo AI Chatbot"
stage: spec
date: 2026-01-16
surface: agent
model: Claude Sonnet 4.5
feature: todo-ai-chatbot
branch: 1-todo-ai-chatbot
user: zuni
command: "/sp.specify"
labels: ["spec", "ai", "chatbot", "mcp"]
links:
  spec: "specs/1-todo-ai-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/1-todo-ai-chatbot/spec.md"
  - "specs/1-todo-ai-chatbot/checklists/requirements.md"
tests: []
---

# Prompt History Record

## Original Prompt

```
This is the **`/sp.specify`** (Technical Specification) for **Phase III: Todo AI Chatbot**. This phase moves your project into the "Architecture of Intelligence" by building a conversational layer over your existing Phase II infrastructure.

Save this as `.spec-kit/specification_phase_3.md`.
***
# 📑 Technical Specification: Todo AI Chatbot (Phase III)
## 1. System Overview
Phase III introduces a conversational interface. Instead of just clicking buttons, users can interact with their tasks via natural language.
- **Protocol:** Model Context Protocol (MCP) will be the "bridge" between the AI and your Task logic.
- **Bot Engine:** OpenAI Agents SDK and Official MCP SDK.
- **Frontend:** OpenAI ChatKit widget embedded in the Next.js dashboard.

## 2. Updated Database Schema (`backend/models.py`)
In addition to the `Task` model from Phase II, we now require persistence for the conversation history to support stateless requests.
### 2.1 `Conversation` Table
- `id`: `int` (Primary Key)
- `user_id`: `str` (Foreign Key -> users.id)
- `created_at`: `datetime`
- `updated_at`: `datetime`

### 2.2 `Message` Table
- `id`: `int` (Primary Key)
- `conversation_id`: `int` (Foreign Key -> conversation.id)
- `role`: `str` (e.g., "user" or "assistant")
- `content`: `text` (The actual message text)
- `created_at`: `datetime`

## 3. MCP Tool Server Specification
The backend must expose the following **MCP Tools** to the AI agent. These tools wrap your existing `TaskManager` logic.

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `add_task` | `title`, `description` | Creates a new todo item for the user. |
| `list_tasks` | `status` (optional) | Retrieves tasks (filter by 'pending', 'completed', or 'all'). |
| `complete_task`| `task_id` | Marks a specific task as complete. |
| `delete_task` | `task_id` | Removes a task from the list. |
| `update_task` | `task_id`, `title`, `description`| Modifies an existing task. |

## 4. Chat API Endpoint (`POST /api/{user_id}/chat`)
This is the main entry point for the ChatKit widget.

**Request Body:**
```json
{
  "conversation_id": 123, // Optional: creates new if null
  "message": "Add a task to buy groceries tomorrow"
}
```

**Execution Flow (Stateless Request Cycle):**
1. **Receive:** User message via API.
2. **Fetch:** Get conversation history from Neon DB.
3. **Initialize:** Start OpenAI Agent with MCP tools.
4. **Invoke:** Agent decides which MCP tool to call (e.g., `add_task`).
5. **Execute:** Tool updates Neon DB.
6. **Respond:** Agent generates a friendly confirmation (e.g., "Done! I've added 'Buy groceries' to your list.")
7. **Store:** Save both user and assistant messages to the `Message` table.

## 5. Agent Behavior Specification
The AI must follow these personality and operational rules:
- **Confirmation:** Always confirm actions (e.g., "I've marked task #5 as complete for you.")
- **Ambiguity:** If a user says "Delete my task" but has 5 tasks, the bot must ask: "Which task would you like me to delete? (Please provide the ID or title)."
- **Conciseness:** Keep responses helpful but brief.
- **Context:** If a user says "What's pending?", use the `list_tasks(status='pending')` tool.

## 6. Frontend Integration (`frontend/`)
- **Widget:** Embed the OpenAI ChatKit widget into the Dashboard.
- **Context Injection:** If a user has a task open/selected, the widget should be able to "see" that context (Selected-Text Support).
- **Styling:** Use Tailwind to ensure the widget matches the Phase II "Stylish" UI.

## 7. Implementation Milestones

### Milestone 1: MCP Foundation
- Install `mcp` and `openai-agents` SDKs in the backend.
- Create `mcp_server.py` and register the 5 core tools.

### Milestone 2: Conversation Persistence
- Implement the `Conversation` and `Message` SQLModel tables.
- Create utility functions to fetch/save chat history.

### Milestone 3: The Chat Loop
- Implement the `/chat` endpoint.
- Connect the AI Agent to the MCP tools.

### Milestone 4: Frontend UI
- Integrate the ChatKit script in the Next.js layout.
- Configure the widget to point to the FastAPI
```

## Response Summary

Created a comprehensive feature specification for the Todo AI Chatbot that includes:
- Overview of the conversational interface system
- Detailed user scenarios and testing flows
- Functional requirements for MCP tools, conversation persistence, chat API, agent behavior, and frontend integration
- Non-functional requirements for performance, security, and reliability
- Key entities (Conversation, Message, Task)
- Success criteria with quantitative and qualitative metrics
- Constraints, dependencies, assumptions, and risk mitigations

The specification captures all the essential elements from the original technical specification while organizing them into a format suitable for planning and implementation.

## Outcome

Successfully created the feature specification document at `specs/1-todo-ai-chatbot/spec.md` with all required sections. Created a quality checklist at `specs/1-todo-ai-chatbot/checklists/requirements.md`. The branch `1-todo-ai-chatbot` has been created and checked out. The specification is ready for the next phase of development.