# Data Model for Todo AI Chatbot

## Entity Definitions

### Conversation
**Purpose:** Represents a session of interaction between user and AI

**Fields:**
- `id` (int, Primary Key, Auto-increment): Unique identifier for the conversation
- `user_id` (str): Foreign key linking to the user who owns this conversation
- `created_at` (datetime): Timestamp when the conversation was initiated
- `updated_at` (datetime): Timestamp of the last activity in this conversation

**Relationships:**
- One-to-Many: Conversation → Messages (one conversation can have many messages)

**Validation Rules:**
- `user_id` must reference an existing user in the system
- `created_at` and `updated_at` should be automatically managed by the ORM

### Message
**Purpose:** Represents a single exchange in a conversation

**Fields:**
- `id` (int, Primary Key, Auto-increment): Unique identifier for the message
- `conversation_id` (int): Foreign key linking to the conversation this message belongs to
- `role` (str): Role of the message sender ('user' or 'assistant')
- `content` (text): The actual text content of the message
- `created_at` (datetime): Timestamp when the message was sent/received

**Relationships:**
- Many-to-One: Message → Conversation (many messages belong to one conversation)

**Validation Rules:**
- `conversation_id` must reference an existing conversation
- `role` must be either 'user' or 'assistant'
- `content` length should be reasonable (not empty, not excessively long)

### Task (Existing from Phase II)
**Purpose:** Represents a todo item managed through the chat interface

**Fields:**
- `id` (int, Primary Key, Auto-increment): Unique identifier for the task
- `title` (str): Title of the task
- `description` (str): Detailed description of the task
- `status` (str): Status of the task ('pending', 'completed')
- `user_id` (str): Foreign key linking to the user who owns this task
- `created_at` (datetime): Timestamp when the task was created
- `updated_at` (datetime): Timestamp of the last update to the task

**Validation Rules:**
- `user_id` must reference an existing user in the system
- `status` must be one of the allowed values ('pending', 'completed')

## State Transitions

### Task Status Transitions
- `pending` → `completed`: When a user completes a task via chat command
- `completed` → `pending`: When a user reopens a completed task via chat command

### Conversation Updates
- `updated_at` is automatically updated whenever a new message is added to the conversation

## Relationships and Constraints

### User Isolation
- All entities (Conversation, Message, Task) must be properly associated with a user_id
- MCP tools must validate that users can only access their own data
- Database queries must always filter by user_id for security

### Referential Integrity
- Messages must have a valid conversation_id pointing to an existing Conversation
- Conversations must have a valid user_id pointing to an existing User
- All foreign key constraints should be enforced at the database level