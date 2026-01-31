"""
Test script to verify real-time updates work when tasks are created through the chatbot.
This script tests the WebSocket functionality and verifies that tasks created via chat
appear in real-time without page refresh.
"""

import asyncio
import websockets
import json
import requests
import time
import threading
import queue
import uuid

# Configuration
BASE_URL = "http://localhost:8000"
WS_BASE_URL = "ws://localhost:8000"

# Test user credentials (will create a test user)
TEST_EMAIL = f"test_chat_{uuid.uuid4()}@example.com"
TEST_PASSWORD = "testpassword123"
TEST_NAME = "Test Chat User"
USER_ID = None
AUTH_TOKEN = None

# Queue to collect WebSocket messages
ws_messages = queue.Queue()

def setup_test_user():
    """Create a test user for testing"""
    global USER_ID, AUTH_TOKEN

    print("Setting up test user...")

    # Signup
    signup_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "name": TEST_NAME
    }

    response = requests.post(f"{BASE_URL}/api/auth/sign-up", json=signup_data)

    if response.status_code == 201:
        data = response.json()
        AUTH_TOKEN = data["token"]
        print("✓ Test user created successfully")

        # Get user ID from token
        import jwt
        decoded = jwt.decode(AUTH_TOKEN, options={"verify_signature": False})
        USER_ID = decoded.get("sub")
        print(f"✓ User ID: {USER_ID}")

        return True
    else:
        print(f"✗ Failed to create test user: {response.text}")
        return False

def test_websocket_connection():
    """Test WebSocket connection and task updates"""
    print(f"\nTesting WebSocket connection for user: {USER_ID}")

    async def listen_for_updates():
        """Listen for WebSocket messages"""
        uri = f"{WS_BASE_URL}/ws/{USER_ID}"

        try:
            async with websockets.connect(uri) as websocket:
                print(f"✓ Connected to WebSocket: {uri}")

                # Wait for messages for a limited time
                try:
                    # Set a timeout for receiving messages
                    message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    print(f"✓ Received message: {message}")

                    # Parse and store the message
                    try:
                        parsed_msg = json.loads(message)
                        ws_messages.put(parsed_msg)
                        return True
                    except json.JSONDecodeError:
                        print(f"✗ Invalid JSON in message: {message}")
                        return False

                except asyncio.TimeoutError:
                    print("⚠ No messages received within timeout period")
                    return True  # This is okay, might not have any updates yet

        except Exception as e:
            print(f"✗ WebSocket connection failed: {e}")
            return False

    # Run the WebSocket test
    return asyncio.run(listen_for_updates())

def test_task_creation_via_chat():
    """Test creating a task via chat and checking for WebSocket updates"""
    print(f"\nTesting task creation via chat for user: {USER_ID}")

    if not AUTH_TOKEN:
        print("✗ No auth token available")
        return False

    # Start WebSocket listener in a separate thread
    def ws_listener():
        asyncio.run(websocket_task_listener())

    ws_thread = threading.Thread(target=ws_listener, daemon=True)
    ws_thread.start()

    time.sleep(1)  # Give WebSocket time to start

    # Create a task via the chat API
    chat_payload = {
        "message": "Create a new task: Buy groceries for the week"
    }

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    print("Sending chat message to create task...")
    response = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload, headers=headers)

    if response.status_code == 200:
        chat_response = response.json()
        print(f"✓ Chat response received: {chat_response['response']}")

        # Check if tool was executed
        if chat_response.get("tool_calls_executed", False):
            print("✓ Tool calls executed (task likely created)")

            # Wait a bit for WebSocket updates
            time.sleep(2)

            # Check if we received any WebSocket messages
            messages_received = []
            while not ws_messages.empty():
                msg = ws_messages.get()
                messages_received.append(msg)

            if messages_received:
                print(f"✓ Received {len(messages_received)} WebSocket message(s)")
                for msg in messages_received:
                    print(f"  - {msg}")

                    # Check if it's a task update
                    if msg.get("event") == "task_update":
                        print("  ✓ Confirmed: Task update received via WebSocket")
                        return True

            print("⚠ No task update messages received via WebSocket")
            return False
        else:
            print("⚠ No tool calls executed - task may not have been created")
            return False
    else:
        print(f"✗ Chat API call failed: {response.status_code} - {response.text}")
        return False

async def websocket_task_listener():
    """Async function to listen for task updates via WebSocket"""
    uri = f"{WS_BASE_URL}/ws/{USER_ID}"

    try:
        async with websockets.connect(uri) as websocket:
            print(f"WebSocket listener connected: {uri}")

            # Listen for messages for a short duration
            try:
                while True:
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    try:
                        parsed_msg = json.loads(message)

                        # Put the message in queue
                        ws_messages.put(parsed_msg)

                        # If it's a task update, we can stop listening
                        if parsed_msg.get("event") == "task_update":
                            print(f"Task update received: {parsed_msg}")
                            break
                    except json.JSONDecodeError:
                        print(f"Invalid JSON: {message}")

            except asyncio.TimeoutError:
                print("WebSocket listener timeout reached")

    except Exception as e:
        print(f"WebSocket listener error: {e}")

def test_get_tasks():
    """Test getting tasks to verify they were created"""
    print(f"\nVerifying tasks were created for user: {USER_ID}")

    if not AUTH_TOKEN:
        print("✗ No auth token available")
        return False

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)

    if response.status_code == 200:
        tasks_data = response.json()
        tasks = tasks_data.get("tasks", [])

        print(f"✓ Retrieved {len(tasks)} tasks")

        # Look for the test task we created
        test_task_found = False
        for task in tasks:
            if "groceries" in task.get("title", "").lower():
                print(f"✓ Found test task: '{task['title']}' (ID: {task['id']})")
                test_task_found = True
                break

        if test_task_found:
            print("✓ Task creation via chat confirmed")
            return True
        else:
            print("⚠ Test task not found in task list")
            return False
    else:
        print(f"✗ Failed to get tasks: {response.status_code} - {response.text}")
        return False

def main():
    """Main test function"""
    print("="*60)
    print("Testing Real-Time Task Updates via Chatbot")
    print("="*60)

    # Step 1: Setup test user
    if not setup_test_user():
        print("✗ Test setup failed")
        return False

    print()

    # Step 2: Test WebSocket connection
    ws_success = test_websocket_connection()

    print()

    # Step 3: Test task creation via chat with WebSocket monitoring
    chat_success = test_task_creation_via_chat()

    print()

    # Step 4: Verify tasks were created
    tasks_success = test_get_tasks()

    print()
    print("="*60)
    print("Test Results:")
    print(f"WebSocket Connection: {'✓ PASS' if ws_success else '✗ FAIL'}")
    print(f"Chat Task Creation: {'✓ PASS' if chat_success else '✗ FAIL'}")
    print(f"Task Verification: {'✓ PASS' if tasks_success else '✗ FAIL'}")

    overall_success = ws_success and chat_success and tasks_success
    print(f"Overall Result: {'✓ ALL TESTS PASSED' if overall_success else '✗ SOME TESTS FAILED'}")
    print("="*60)

    return overall_success

if __name__ == "__main__":
    # Check if backend is running first
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            print(f"✓ Backend is running at {BASE_URL}")
            main()
        else:
            print(f"✗ Backend not accessible at {BASE_URL}")
            print("Please start the backend server before running this test.")
    except requests.exceptions.RequestException:
        print(f"✗ Backend not accessible at {BASE_URL}")
        print("Please start the backend server before running this test.")