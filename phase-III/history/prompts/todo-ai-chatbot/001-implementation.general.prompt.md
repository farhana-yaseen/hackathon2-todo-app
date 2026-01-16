---
id: 1
title: "AI Chatbot Implementation"
stage: "general"
date_iso: "2026-01-16"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-ai-chatbot"
branch: "1-todo-ai-chatbot"
user: "claude"
command: "sp.plan (manual execution)"
labels: ["ai", "chatbot", "backend", "frontend", "integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - .spec-kit/plan_phase_3.md
  - backend/openrouter_client.py
  - backend/chat_logic.py
  - backend/models.py
  - backend/routes/chat.py
  - backend/main.py
  - frontend/lib/api.ts
  - frontend/components/ChatComponent.tsx
  - frontend/app/page.tsx
tests_yaml: |
  - backend/test_chat_endpoints.py
  - frontend/test_chat_component.tsx
---

# AI Chatbot Implementation

## PROMPT_TEXT

```
This is the **`/sp.plan` (Implementation Plan)** for your Phase III Todo AI Chatbot. This plan breaks down the technical specification into a logical sequence of coding tasks for **Claude Code** to follow.
Save this as: `.spec-kit/plan_phase_3.md`
***
# 🛠 Implementation Plan: Phase III AI Chatbot
## Phase 1: Environment & Dependencies
- [ ] **Install Dependencies:** Add `mcp`, `openai`, and `openai-agents` to the backend (via `uv` or `pip`).
- [ ] **Environment Setup:** Ensure `COHERE_API_KEY` and `DATABASE_URL` are configured in the `.env` file.
- [ ] **SDK Configuration:** Create a utility to initialize the `OpenAI` client pointing to `https://openrouter.ai/api/v1`.

## Phase 2: Database & Persistence
- [ ] **Update Models (`backend/models.py`):**
    - [ ] Implement `Conversation` class (id, user_id, timestamps).
    - [ ] Implement `Message` class (id, conversation_id, role, content, timestamps).
- [ ] **Database Migration:** Run migrations to create the new tables in Neon DB.
- [ ] **History Helpers:*n:** Ensure tools correctly identify the `user_id` context to prevent one user from modifying another's tasks.

## Phase 4: The Agentic Chat Endpoint
- [ ] **Create Chat Service (`backend/chat_logic.py`):**
    - [ ] Define the `Agent` instructions (System Prompt).
    - [ ] Initialize the `openai-agents` `Runner`.
- [ ] **Implement Endpoint (`POST /api/{user_id}/chat`):**
    - [ ] Extract user message and `conversation_id`.
    - [ ] Fetch history from DB.
    - [ ] Run the Agentic Loop: `Runner.run(agent, history, tools)`.
    - [ ] Persist the final user and assistant messages to the DB.
    - [ ] Return the response JSON.

## Phase 5: Frontend Integration
- [ ] **ChatKit Integration:**
    - [ ] Add the OpenAI ChatKit script/component to the Next.js layout.
    - [ ] Configure the widget to send requests to the FastAPI backend.
- [ ] **UI/UX Polish:**
    - [ ] Ensure the chat bubble matches the dashboard theme.
    - [ ] Add a "Clear Conversation" button to start a new `conversation_id`.
    - [ ] Handl
```

## RESPONSE_TEXT

Implemented the complete AI chatbot feature for the Todo application. Created backend infrastructure including:

- Updated models.py with Conversation and Message classes
- Created Cohere client utility for AI integration
- Built chat_logic.py with AI agent instructions and tool integration
- Implemented chat API endpoints with conversation management
- Added frontend ChatComponent with conversation history and UI
- Extended API client with chat functionality

The AI assistant can now help users manage their tasks using natural language, with full conversation persistence and user isolation.

## OUTCOME

Successfully implemented the AI chatbot feature with both backend and frontend components. The chatbot integrates seamlessly with the existing task management system and provides natural language interaction for task management.

## EVALUATION

The implementation follows the planned architecture with proper separation of concerns. The AI assistant can perform CRUD operations on tasks through natural language, with appropriate security measures to ensure user data isolation.