# ✅ Implementation Tasks: Phase III AI Chatbot

## 1. Project Initialization & Dependencies
- [x] T001 Install backend dependencies: `pip install cohere` in backend directory
- [x] T002 Add `COHERE_API_KEY` to `.env` file in backend directory
- [x] T003 Verify `DATABASE_URL` for Neon DB is active and reachable
- [x] T004 Create Cohere client utility in `backend/cohere_client.py`

## 2. Database Model Extensions
- [x] T005 [US1] Add `Conversation` class to `backend/models.py` with fields: `id`, `user_id`, `title`, `created_at`, `updated_at`
- [x] T006 [US1] Add `Message` class to `backend/models.py` with fields: `id`, `conversation_id`, `role`, `content`, `created_at`
- [x] T007 [US1] Update `SQLModel.metadata.create_all(engine)` logic to ensure new tables are created
- [x] T008 [US1] Add indexes for efficient querying: `idx_conversations_user_created`, `idx_messages_conversation_created`

## 3. AI Agent & Chat Logic
- [x] T009 [US1] Create `backend/chat_logic.py` with chat service implementation
- [x] T010 [US1] Define the `System Prompt` for the AI assistant with tool descriptions
- [x] T011 [US1] Implement Cohere client integration with tool calling capability
- [x] T012 [US1] Implement tool functions: `add_task`, `list_tasks`, `complete_task`, `update_task`, `delete_task`
- [x] T013 [US1] Implement conversation management and message persistence

## 4. Backend API Integration
- [x] T014 [US1] Create the router/endpoint `POST /api/{user_id}/chat`
- [x] T015 [US1] Implement logic to check for existing `conversation_id`; create new if none provided
- [x] T016 [US1] Implement logic to load history from DB and call chat service
- [x] T017 [US1] Implement logic to save user input and AI response to `Message` table
- [x] T018 [US1] Return JSON response: `{"conversation_id": int, "response": str, "tool_calls_executed": bool, "timestamp": str}`
- [x] T019 [US1] Add GET endpoint for listing conversations: `GET /api/{user_id}/conversations`
- [x] T020 [US1] Add GET endpoint for conversation messages: `GET /api/{user_id}/conversations/{conversation_id}/messages`
- [x] T021 [US1] Add DELETE endpoint for conversation: `DELETE /api/{user_id}/conversations/{conversation_id}`

## 5. Frontend API Client Extension
- [x] T022 [US2] Add chat API functions to `frontend/lib/api.ts`: `chatWithAI`
- [x] T023 [US2] Add conversation management functions to `frontend/lib/api.ts`: `getConversations`, `getConversationMessages`, `deleteConversation`
- [x] T024 [US2] Update API client to handle chat-specific request/response types

## 6. Frontend Chat Interface
- [x] T025 [US2] Create ChatComponent in `frontend/components/ChatComponent.tsx`
- [x] T026 [US2] Implement chat UI with conversation sidebar and message display
- [x] T027 [US2] Add chat input with send functionality
- [x] T028 [US2] Implement conversation management UI (new, delete, switch)
- [x] T029 [US2] Add loading states and error handling to chat component
- [x] T030 [US2] Integrate ChatComponent with main dashboard page in `frontend/app/page.tsx`

## 7. Integration & Testing
- [x] T031 [US3] Test end-to-end chat functionality with task management tools
- [x] T032 [US3] Verify user isolation - users can only access their own conversations
- [x] T033 [US3] Test conversation persistence across sessions
- [x] T034 [US3] Verify proper error handling and validation

## Dependencies
- User Story 1 (Backend): Tasks T001-T021 depend on foundational setup (T001-T004)
- User Story 2 (Frontend): Tasks T022-T030 depend on API endpoints (T014-T021)
- User Story 3 (Integration): Tasks T031-T034 depend on both backend and frontend (T005-T030)

## Parallel Execution Opportunities
- [P] Tasks T005-T008 (Database models) can run in parallel with T009-T013 (Chat logic)
- [P] Tasks T022-T024 (API extensions) can run in parallel with T025-T029 (UI components)

## Implementation Strategy
- MVP Scope: Basic chat functionality with task management tools (US1 + US2)
- Incremental Delivery:
  1. Backend foundation and API (T001-T021)
  2. Frontend integration (T022-T030)
  3. Full integration testing (T031-T034)