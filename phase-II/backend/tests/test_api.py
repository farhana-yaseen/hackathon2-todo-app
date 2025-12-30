"""Tests for Todo API endpoints.

This module tests all API endpoints including authentication and task CRUD operations.
"""
import os
import sys
import uuid

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

# Import routers
from api.routes.tasks import router as tasks_router
from api.routes.auth import router as auth_router


# Create FastAPI app for testing
app = FastAPI()

# Add health endpoint for testing
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": "todo-backend"}

app.include_router(tasks_router)
app.include_router(auth_router)


def generate_unique_email():
    """Generate a unique email for each test."""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def fresh_db():
    """Reset the in-memory database before each test."""
    from api.routes.auth import _users_db
    _users_db.clear()
    yield
    _users_db.clear()


@pytest.fixture
def unique_user(fresh_db):
    """Return a unique test user data."""
    return {
        "email": generate_unique_email(),
        "password": "testpassword123",
        "name": "Test User"
    }


@pytest.fixture
def client(fresh_db):
    """Create a test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "todo-backend"


class TestAuthEndpoints:
    """Tests for authentication endpoints."""

    def test_sign_up(self, client, unique_user):
        """Test user registration."""
        response = client.post(
            "/api/auth/sign-up",
            json=unique_user
        )
        assert response.status_code == 201
        data = response.json()
        assert data["user"]["email"] == unique_user["email"]
        assert data["user"]["name"] == unique_user["name"]
        assert "token" in data
        assert len(data["token"]) > 0

    def test_sign_up_duplicate_email(self, client, unique_user):
        """Test that duplicate email registration fails."""
        # First signup should succeed
        response = client.post("/api/auth/sign-up", json=unique_user)
        assert response.status_code == 201

        # Second signup with same email should fail
        response = client.post("/api/auth/sign-up", json=unique_user)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_sign_in_success(self, client, unique_user):
        """Test successful sign in."""
        # First create the user
        sign_up_response = client.post("/api/auth/sign-up", json=unique_user)
        assert sign_up_response.status_code == 201

        # Then sign in
        response = client.post(
            "/api/auth/sign-in",
            json={"email": unique_user["email"], "password": unique_user["password"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == unique_user["email"]
        assert "token" in data

    def test_sign_in_wrong_password(self, client, unique_user):
        """Test sign in with wrong password fails."""
        # First create the user
        client.post("/api/auth/sign-up", json=unique_user)

        # Then try sign in with wrong password
        response = client.post(
            "/api/auth/sign-in",
            json={"email": unique_user["email"], "password": "wrongpassword"}
        )
        assert response.status_code == 401

    def test_sign_in_nonexistent_user(self, client):
        """Test sign in with nonexistent user fails."""
        response = client.post(
            "/api/auth/sign-in",
            json={"email": "nonexistent@example.com", "password": "password123"}
        )
        assert response.status_code == 401

    def test_get_session_with_token(self, client, unique_user):
        """Test getting session with valid token."""
        # Create and sign in user
        sign_up_response = client.post("/api/auth/sign-up", json=unique_user)
        token = sign_up_response.json()["token"]

        # Get session with token
        response = client.get(
            "/api/auth/session",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == unique_user["email"]
        assert data["token"] == token

    def test_get_session_without_token(self, client):
        """Test getting session without token fails."""
        response = client.get("/api/auth/session")
        assert response.status_code == 401

    def test_sign_out(self, client, unique_user):
        """Test sign out clears session."""
        # Create user and sign in
        sign_up_response = client.post("/api/auth/sign-up", json=unique_user)
        assert sign_up_response.status_code == 201

        # Sign out
        response = client.post("/api/auth/sign-out")
        assert response.status_code == 200


class TestTaskEndpoints:
    """Tests for task CRUD endpoints."""

    def test_create_task(self, client, unique_user):
        """Test creating a new task."""
        # Sign up and get token
        sign_up_response = client.post("/api/auth/sign-up", json=unique_user)
        token = sign_up_response.json()["token"]

        # Create task
        response = client.post(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Test Task", "description": "Test description"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test description"
        assert data["completed"] == False
        assert "id" in data
        assert "user_id" in data

    def test_create_task_without_auth(self, client):
        """Test creating task without auth fails."""
        response = client.post(
            "/api/tasks",
            json={"title": "Test Task"}
        )
        assert response.status_code == 401

    def test_list_tasks(self, client, unique_user):
        """Test listing tasks for authenticated user."""
        # Sign up and get token
        sign_up_response = client.post("/api/auth/sign-up", json=unique_user)
        token = sign_up_response.json()["token"]

        # Create some tasks
        client.post("/api/tasks", headers={"Authorization": f"Bearer {token}"}, json={"title": "Task 1"})
        client.post("/api/tasks", headers={"Authorization": f"Bearer {token}"}, json={"title": "Task 2"})

        # List tasks
        response = client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert data["total"] >= 2

    def test_get_task(self, client, unique_user):
        """Test getting a specific task."""
        # Sign up and get token
        sign_up_response = client.post("/api/auth/sign-up", json=unique_user)
        token = sign_up_response.json()["token"]

        # Create task
        create_response = client.post(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Test Task"}
        )
        task_id = create_response.json()["id"]

        # Get task
        response = client.get(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test Task"

    def test_update_task(self, client, unique_user):
        """Test updating a task."""
        # Sign up and get token
        sign_up_response = client.post("/api/auth/sign-up", json=unique_user)
        token = sign_up_response.json()["token"]

        # Create task
        create_response = client.post(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Original Title"}
        )
        task_id = create_response.json()["id"]

        # Update task
        response = client.put(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Updated Title", "description": "Updated description"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"

    def test_toggle_complete(self, client, unique_user):
        """Test toggling task completion."""
        # Sign up and get token
        sign_up_response = client.post("/api/auth/sign-up", json=unique_user)
        token = sign_up_response.json()["token"]

        # Create task
        create_response = client.post(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Test Task"}
        )
        task_id = create_response.json()["id"]

        # Toggle complete
        response = client.patch(
            f"/api/tasks/{task_id}/complete",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] == True

        # Toggle again
        response = client.patch(
            f"/api/tasks/{task_id}/complete",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] == False

    def test_delete_task(self, client, unique_user):
        """Test deleting a task."""
        # Sign up and get token
        sign_up_response = client.post("/api/auth/sign-up", json=unique_user)
        token = sign_up_response.json()["token"]

        # Create task
        create_response = client.post(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Task to delete"}
        )
        task_id = create_response.json()["id"]

        # Delete task
        response = client.delete(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["success"] == True

        # Task should no longer exist
        get_response = client.get(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert get_response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
