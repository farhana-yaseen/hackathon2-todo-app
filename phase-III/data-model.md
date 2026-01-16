# Data Model: AI Chatbot

## Entities

### Conversation
Represents a single conversation thread between a user and the AI assistant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | int | Primary Key, Auto-increment | Unique identifier for the conversation |
| user_id | str | Not Null, Indexed | User ID from JWT token (matches Better Auth) |
| title | str | Optional, Max 200 chars | Auto-generated title from first message |
| created_at | datetime | Not Null, Default now | Timestamp when conversation was created |
| updated_at | datetime | Not Null, Default now | Timestamp when conversation was last updated |

### Message
Represents a single message within a conversation (from user or AI).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | int | Primary Key, Auto-increment | Unique identifier for the message |
| conversation_id | int | Not Null, Foreign Key, Indexed | Reference to parent conversation |
| role | str | Not Null, Enum('user','assistant','system') | Who sent this message |
| content | str | Not Null, Max 10000 chars | The actual message content |
| created_at | datetime | Not Null, Default now | Timestamp when message was created |

## Relationships
- Conversation (1) ←→ (Many) Message
- Message.conversation_id → Conversation.id (Foreign Key)

## Indexes
- idx_conversations_user_created: (user_id, created_at) - For efficient user conversation listing
- idx_messages_conversation_created: (conversation_id, created_at) - For efficient message retrieval

## Validation Rules
- Conversation.user_id must match authenticated user's ID
- Message.role must be one of 'user', 'assistant', or 'system'
- Message.content cannot be empty
- Conversation timestamps are automatically managed

## State Transitions
- Conversation is created when user starts a new chat
- Messages are added to conversation as user and AI exchange messages
- Conversation is implicitly updated when new messages are added