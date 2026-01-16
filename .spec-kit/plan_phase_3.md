# 🛠 Implementation Plan: Phase III AI Chatbot
## Phase 1: Environment & Dependencies
- [ ] **Install Dependencies:** Add `mcp`, `openai`, and `openai-agents` to the backend (via `uv` or `pip`).
- [ ] **Environment Setup:** Ensure `OPENROUTER_API_KEY` and `DATABASE_URL` are configured in the `.env` file.
- [ ] **SDK Configuration:** Create a utility to initialize the `OpenAI` client pointing to `https://openrouter.ai/api/v1`.

## Phase 2: Database & Persistence
- [ ] **Update Models (`backend/models.py`):**
    - [ ] Implement `Conversation` class (id, user_id, timestamps).
    - [ ] Implement `Message` class (id, conversation_id, role, content, timestamps).
- [ ] **Database Migration:** Run migrations to create the new tables in Neon DB.
- [ ] **History Helpers:** Create functions to:
    - [ ] `get_chat_history(conversation_id)`: Retrieve last 10-20 messages.
    - [ ] `save_chat_message(conversation_id, role, content)`: Persist new interactions.

## Phase 3: MCP Tool Implementation
- [ ] **Create MCP Server (`backend/mcp_server.py`):**
    - [ ] Define the `add_task` tool (wraps existing SQLModel logic).
    - [ ] Define the `list_tasks` tool (with status filtering).
    - [ ] Define `complete_task`, `delete_task`, and `update_task` tools.
- [ ] **Validation:** Ensure tools correctly identify the `user_id` context to prevent one user from modifying another's tasks.

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
    - [ ] Handle "Loading" states while the AI is "thinking" or calling tools.

## Phase 6: Testing & Validation
- [ ] **Functional Test:** "Add a task to buy groceries" -> Verify task appears in the DB.
- [ ] **Filtering Test:** "Show me my completed tasks" -> Verify AI calls `list_tasks(status='completed')`.
- [ ] **Persistence Test:** Refresh the page -> Verify the chat history remains visible in the widget.