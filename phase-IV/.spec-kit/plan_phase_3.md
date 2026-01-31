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
- [ ] **History Helpers:** Ensure tools correctly identify the `user_id` context to prevent one user from modifying another's tasks.

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
    - [ ] Handle edge cases and error states gracefully.