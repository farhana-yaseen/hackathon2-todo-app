# Todo App - Phase IV
A full-stack todo application with advanced features: user authentication, real-time synchronization, AI chatbot integration, and enhanced security.

## Project Overview
This is a monorepo containing a Next.js 14 frontend and FastAPI backend, following spec-driven development practices with GitHub Spec-Kit. Phase IV introduces AI-powered task management through an integrated chatbot with real-time updates.

## Tech Stack

### Frontend
- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **Better Auth** - Authentication
- **React 19**

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM
- **PostgreSQL** (Neon) - Database
- **JWT** - Token-based authentication
- **Pydantic** - Data validation
- **Python 3.13+**
- **Cohere** - AI Integration
- **WebSocket** - Real-time updates

## Features

- User authentication (signup/login) with OAuth (Google/GitHub)
- Create, read, update, delete tasks
- Mark tasks as complete/pending
- Persistent storage with PostgreSQL
- RESTful API design
- Type-safe TypeScript frontend
- Modern responsive UI
- AI-powered chatbot for task management
- Real-time task synchronization via WebSockets
- Cross-domain authentication support
- Email verification and password reset
- Conversation history with AI assistant
- Task categorization and filtering

## Project Structure

```
phase-IV/
├── frontend/          # Next.js application
│   ├── app/          # Next.js pages and layouts
│   ├── components/   # Reusable UI components
│   └── lib/          # API client and utilities
├── backend/          # FastAPI application
│   ├── src/
│   │   ├── api/     # API route handlers
│   │   └── models/  # Database models
│   ├── chat_logic.py # AI chat logic
│   ├── cohere_client.py # Cohere integration
│   └── tests/       # Backend tests
├── specs/           # Specification documents
└── .spec-kit/       # Spec-driven development artifacts
```

## Getting Started

### Prerequisites

- Node.js 20+ and npm
- Python 3.13+
- PostgreSQL database (or Neon account)
- API keys for AI services (Cohere)

### Environment Setup

1. **Backend Environment Variables**

Create `backend/.env`:
```env
DATABASE_URL=postgresql://user:password@host/dbname
BETTER_AUTH_SECRET=your-secret-key-here
COHERE_API_KEY=your-cohere-api-key
SESSION_SECRET=your-session-secret
FRONTEND_URL=https://your-frontend-url.com
```

2. **Frontend Environment Variables**

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Installation

#### Backend Setup

```bash
cd backend
pip install -e .
```

#### Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Development Mode

**Backend (Terminal 1):**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Using Docker Compose (Alternative)

```bash
docker-compose up
```

## Advanced Features

### AI Chatbot Integration
- Natural language task management through the integrated chatbot
- Conversational interface for creating, updating, and managing tasks
- Context-aware responses based on user's task history

### Real-time Updates
- WebSocket-based real-time synchronization
- Instant updates when tasks are created via chatbot
- No page refresh required for new tasks to appear

### Authentication Enhancements
- Cross-domain cookie support for microservices deployment
- OAuth integration with Google and GitHub
- Email verification and secure password reset
- Session management with proper security headers

## Development Guidelines

### Backend Development

See [backend/CLAUDE.md](backend/CLAUDE.md) for:
- API conventions
- Database patterns
- Code standards

### Frontend Development

See [frontend/CLAUDE.md](frontend/CLAUDE.md) for:
- Component patterns
- API client usage
- Styling guidelines

### Spec-Driven Development

This project follows spec-driven development:

1. **Read specs first**: Check `specs/` directory before implementing
2. **Reference specs**: Use `@specs/features/[feature].md` syntax
3. **Update specs**: Keep specifications in sync with implementation

Spec organization:
- `specs/features/` - Feature requirements
- `specs/api/` - API endpoints and contracts
- `specs/database/` - Database schema
- `specs/ui/` - UI components and pages

## Testing

### Backend Tests

```bash
cd backend
pytest tests/

# With coverage
pytest tests/ --cov=src --cov-report=term-missing
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Code Quality

### Backend

```bash
# Type checking
mypy src/

# Linting
ruff check src/

# Format code
ruff format src/
```

### Frontend

```bash
# Linting
npm run lint

# Type checking
npm run type-check
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Contributing

1. Check existing specs in `specs/` directory
2. Follow the development guidelines in CLAUDE.md files
3. Write tests for new features
4. Ensure code quality checks pass

## Important Notes

- **Environment Files**: Never commit `.env` files to version control
- **Database**: Ensure PostgreSQL is running before starting the backend
- **API URL**: Update `NEXT_PUBLIC_API_URL` in frontend `.env.local` if backend runs on different port
- **Security**: All authentication cookies are configured for cross-domain requests with proper security attributes

## License

This project is part of a hackathon submission.