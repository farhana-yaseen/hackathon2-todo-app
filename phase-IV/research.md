# Research Document: AI Chatbot Implementation

## Unknowns Identified

### 1. MCP Server Integration
- **Unknown**: Current MCP (Model Context Protocol) server setup and integration patterns
- **Clarification Needed**: How to properly set up an MCP server for our FastAPI backend
- **Decision**: Will implement using standard Python MCP protocol libraries
- **Rationale**: MCP will allow the AI to call our backend functions as tools
- **Alternatives Considered**: Direct function calling vs MCP standard vs custom API

### 2. OpenAI Agents vs OpenRouter
- **Unknown**: Whether to use OpenAI's agents framework or OpenRouter's API
- **Decision**: Use OpenRouter API with their compatible endpoints since we already have OPENROUTER_API_KEY
- **Rationale**: OpenRouter supports various models and is already configured in our environment
- **Alternatives Considered**: OpenAI API, Anthropic Claude, local models

### 3. Conversation and Message Model Structure
- **Unknown**: Exact fields needed for Conversation and Message models
- **Decision**: Extend existing models to include user_id, timestamps, and proper relationships
- **Rationale**: Following the same pattern as existing Task model for consistency
- **Alternatives Considered**: Separate service vs extending existing models

### 4. Frontend Chat Integration
- **Unknown**: How to integrate OpenAI ChatKit or similar widget with Next.js
- **Decision**: Create custom chat interface that communicates with our backend endpoint
- **Rationale**: More control over the UI/UX and integration with our authentication system
- **Alternatives Considered**: OpenAI ChatKit, third-party widgets, iframe integration

### 5. Authentication for Chat Endpoint
- **Unknown**: How to ensure chat endpoints respect user isolation
- **Decision**: Use the same JWT authentication pattern as existing endpoints
- **Rationale**: Consistency with existing security model
- **Alternatives Considered**: Session-based, API keys, separate auth system

## Technology Choices

### Dependencies to Install
- `openai` - for OpenRouter API integration
- `mcp` - for Model Context Protocol server (if needed)
- Potentially other dependencies based on implementation approach

### Database Models
- `Conversation` model with fields: id, user_id, created_at, updated_at
- `Message` model with fields: id, conversation_id, role (user/assistant), content, created_at
- Proper foreign key relationships and indexing

### API Endpoint Structure
- `POST /api/{user_id}/chat` - Main chat endpoint
- Will include conversation_id in request body
- Will return streaming or complete response