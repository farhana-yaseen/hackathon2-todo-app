"""
AI Chat Logic for the Todo Application
"""
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import json

from cohere import ChatMessage
from sqlmodel import Session, select
from models import Conversation, Message, Task, User
from cohere_client import cohere_client


class ChatService:
    """
    Service class to handle AI chat logic and conversation management
    """
    def __init__(self):
        self.co = cohere_client.get_client()

    def get_system_prompt(self) -> str:
        """
        Returns the system prompt for the AI assistant
        """
        return """
        You are an AI assistant integrated with a Todo application. Your purpose is to help users manage their tasks and conversations.

        You have access to the following tools:
        1. add_task: Create a new task for the user
        2. list_tasks: Get all tasks for the user
        3. complete_task: Mark a task as completed
        4. update_task: Modify an existing task
        5. delete_task: Remove a task

        When using these tools, make sure to:
        - Respect the user's privacy and only access their own data
        - Follow the user's instructions for managing their tasks
        - Provide helpful and concise responses
        - If a user asks about something outside of these capabilities, politely explain what you can do

        Always be helpful, friendly, and professional.
        """

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Defines the tools available to the AI assistant
        """
        return [
            {
                "name": "add_task",
                "description": "Create a new task for the user",
                "parameter_definitions": {
                    "title": {
                        "description": "The title of the task",
                        "type": "str",
                        "required": True
                    },
                    "description": {
                        "description": "Optional description of the task",
                        "type": "str",
                        "required": False
                    },
                    "category": {
                        "description": "Optional category for the task (e.g., Work, Personal)",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "list_tasks",
                "description": "Get all tasks for the user",
                "parameter_definitions": {}
            },
            {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to complete",
                        "type": "int",
                        "required": True
                    }
                }
            },
            {
                "name": "update_task",
                "description": "Modify an existing task",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to update",
                        "type": "int",
                        "required": True
                    },
                    "title": {
                        "description": "New title for the task",
                        "type": "str",
                        "required": False
                    },
                    "description": {
                        "description": "New description for the task",
                        "type": "str",
                        "required": False
                    },
                    "category": {
                        "description": "New category for the task",
                        "type": "str",
                        "required": False
                    },
                    "completed": {
                        "description": "Whether the task is completed",
                        "type": "bool",
                        "required": False
                    }
                }
            },
            {
                "name": "delete_task",
                "description": "Remove a task",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to delete",
                        "type": "int",
                        "required": True
                    }
                }
            }
        ]

    async def handle_tool_calls(self, tool_calls: List[Dict], user_id: str, session: Session) -> List[Dict]:
        """
        Handle tool calls from the AI assistant
        """
        results = []

        for tool_call in tool_calls:
            tool_name = tool_call['name']
            parameters = tool_call['parameters']

            if tool_name == "add_task":
                task = Task(
                    user_id=user_id,
                    title=parameters.get('title'),
                    description=parameters.get('description'),
                    category=parameters.get('category'),
                    completed=False
                )
                session.add(task)
                session.commit()
                session.refresh(task)

                results.append({
                    "call": tool_call,
                    "outputs": [{"result": f"Task '{task.title}' (ID: {task.id}) has been created successfully."}]
                })

            elif tool_name == "list_tasks":
                statement = select(Task).where(Task.user_id == user_id)
                tasks = session.exec(statement).all()

                task_list = []
                for task in tasks:
                    task_list.append({
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "category": task.category,
                        "due_date": task.due_date.isoformat() if task.due_date else None
                    })

                results.append({
                    "call": tool_call,
                    "outputs": [{"result": f"Found {len(task_list)} tasks", "tasks": task_list}]
                })

            elif tool_name == "complete_task":
                task_id = parameters.get('task_id')
                statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                task = session.exec(statement).first()

                if task:
                    task.completed = True
                    session.add(task)
                    session.commit()

                    results.append({
                        "call": tool_call,
                        "outputs": [{"result": f"Task '{task.title}' (ID: {task.id}) has been marked as completed."}]
                    })
                else:
                    results.append({
                        "call": tool_call,
                        "outputs": [{"error": f"Task with ID {task_id} not found or doesn't belong to user."}]
                    })

            elif tool_name == "update_task":
                task_id = parameters.get('task_id')
                statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                task = session.exec(statement).first()

                if task:
                    # Update fields if provided
                    if 'title' in parameters:
                        task.title = parameters['title']
                    if 'description' in parameters:
                        task.description = parameters['description']
                    if 'category' in parameters:
                        task.category = parameters['category']
                    if 'completed' in parameters:
                        task.completed = parameters['completed']

                    session.add(task)
                    session.commit()

                    results.append({
                        "call": tool_call,
                        "outputs": [{"result": f"Task '{task.title}' (ID: {task.id}) has been updated successfully."}]
                    })
                else:
                    results.append({
                        "call": tool_call,
                        "outputs": [{"error": f"Task with ID {task_id} not found or doesn't belong to user."}]
                    })

            elif tool_name == "delete_task":
                task_id = parameters.get('task_id')
                statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                task = session.exec(statement).first()

                if task:
                    title = task.title
                    session.delete(task)
                    session.commit()

                    results.append({
                        "call": tool_call,
                        "outputs": [{"result": f"Task '{title}' (ID: {task_id}) has been deleted successfully."}]
                    })
                else:
                    results.append({
                        "call": tool_call,
                        "outputs": [{"error": f"Task with ID {task_id} not found or doesn't belong to user."}]
                    })
            else:
                results.append({
                    "call": tool_call,
                    "outputs": [{"error": f"Unknown tool: {tool_name}"}]
                })

        return results

    async def chat(self, user_id: str, message_content: str, conversation_id: Optional[int], session: Session) -> Dict[str, Any]:
        """
        Main chat method that handles the conversation with the AI
        """
        # Get or create conversation
        if conversation_id:
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise ValueError("Invalid conversation ID or unauthorized access")
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id, title=message_content[:100] if len(message_content) > 100 else message_content)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            conversation_id = conversation.id

        # Add user message to conversation
        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=message_content
        )
        session.add(user_message)
        session.commit()

        # Get conversation history
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        messages = session.exec(statement).all()

        # Prepare messages for Cohere
        cohere_messages = []
        for msg in messages:
            cohere_messages.append(ChatMessage(role=msg.role, message=msg.content))

        # Call Cohere chat endpoint with tools
        try:
            response = self.co.chat(
                message=message_content,
                chat_history=cohere_messages[:-1],  # Exclude the current message
                preamble=self.get_system_prompt(),
                tools=self.get_available_tools(),
                model="command-light"
            )
        except Exception as e:
            # Log the error for debugging
            print(f"Cohere API error: {str(e)}")
            # Return a user-friendly error message
            response = type('obj', (object,), {'text': 'Sorry, I am currently experiencing high demand or technical issues. Please try again in a moment.'})()

        # Handle tool calls if any
        if hasattr(response, 'tool_calls') and response.tool_calls:
            tool_results = await self.handle_tool_calls(response.tool_calls, user_id, session)

            # Get the final response after tool execution
            try:
                response = self.co.chat(
                    message=message_content,
                    chat_history=cohere_messages[:-1] + [ChatMessage(role="assistant", message=str(response.text))],
                    preamble=self.get_system_prompt(),
                    tools=self.get_available_tools(),
                    tool_results=tool_results,
                    model="command-light"
                )
            except Exception as e:
                # Log the error for debugging
                print(f"Cohere API error after tool execution: {str(e)}")
                # Return a user-friendly error message
                response = type('obj', (object,), {'text': 'Sorry, I encountered an issue processing your request after using tools. Please try again.'})()

        # Add assistant response to conversation
        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=response.text if hasattr(response, 'text') else str(response)
        )
        session.add(assistant_message)
        session.commit()

        # Update conversation's updated_at timestamp
        conversation.updated_at = datetime.now(timezone.utc)
        session.add(conversation)
        session.commit()

        return {
            "conversation_id": conversation_id,
            "response": response.text if hasattr(response, 'text') else str(response),
            "tool_calls_executed": bool(getattr(response, 'tool_calls', []))
        }


# Global instance
chat_service = ChatService()