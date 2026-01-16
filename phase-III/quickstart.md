# Quickstart Guide: AI Chatbot Implementation

## Prerequisites

### Environment Variables
Ensure the following environment variables are set in your `.env` file:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
DATABASE_URL=your_neon_postgres_connection_string
BETTER_AUTH_SECRET=your_shared_secret_for_jwt_verification
```

### Dependencies
Install required packages:
```bash
cd backend
uv pip install openai
```

## Database Setup

### New Models
Two new models will be added to `models.py`:
1. `Conversation` - stores conversation metadata
2. `Message` - stores individual messages in conversations

### Migration
Database migration will be handled automatically with existing patterns in `main.py`.

## Backend Implementation

### 1. MCP Server (`backend/mcp_server.py`)
Will define tools that the AI can call:
- `add_task` - Create new tasks
- `list_tasks` - Retrieve user's tasks
- `complete_task` - Mark tasks as complete
- `delete_task` - Remove tasks
- `update_task` - Modify existing tasks

### 2. Chat Logic (`backend/chat_logic.py`)
Contains the AI agent configuration and conversation handling logic.

### 3. API Endpoint (`backend/routes/chat.py`)
New route file with:
- `POST /api/{user_id}/chat` - Main chat endpoint
- `GET /api/{user_id}/conversations` - List user's conversations
- `GET /api/{user_id}/conversations/{conversation_id}/messages` - Get conversation messages

## Frontend Integration

### 1. Chat Component
A new React component will be created in the frontend that:
- Communicates with the backend chat endpoint
- Maintains conversation history
- Shows loading states during AI processing

### 2. Authentication
The chat component will use existing authentication patterns with JWT tokens.

## Running the Application

### Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

## Testing

### Unit Tests
Tests will be added for:
- Database models
- API endpoints
- MCP tools
- Authentication middleware

### Integration Tests
End-to-end tests for:
- Creating conversations
- Sending messages
- Tool calling functionality
- User isolation