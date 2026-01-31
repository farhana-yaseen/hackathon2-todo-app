"""
Chat API Routes for the Todo Application
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import datetime
from pydantic import BaseModel

from db import get_session
from models import Conversation, Message
from chat_logic import chat_service
from db import require_auth, AuthenticatedUser


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str


router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    conversation_id: Optional[int] = None,
    session: Session = Depends(get_session),
    user_data: AuthenticatedUser = Depends(require_auth)
):
    """
    Main chat endpoint that handles conversation with the AI assistant

    Args:
        user_id: The ID of the user (should match the authenticated user)
        message: The user's message to the AI
        conversation_id: Optional conversation ID to continue an existing conversation
        session: Database session
        user_data: Authenticated user data

    Returns:
        dict: Response from the AI assistant and conversation ID
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Cannot access another user's chat"
        )

    try:
        result = await chat_service.chat(
            user_id=user_id,
            message_content=request.message,
            conversation_id=conversation_id,
            session=session
        )

        return {
            "conversation_id": result["conversation_id"],
            "response": result["response"],
            "tool_calls_executed": result["tool_calls_executed"],
            "timestamp": datetime.utcnow().isoformat()
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


@router.get("/{user_id}/conversations")
async def list_conversations(
    user_id: str,
    session: Session = Depends(get_session),
    user_data: AuthenticatedUser = Depends(require_auth)
):
    """
    List all conversations for a user

    Args:
        user_id: The ID of the user (should match the authenticated user)
        session: Database session
        user_data: Authenticated user data

    Returns:
        list: List of user's conversations
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Cannot access another user's conversations"
        )

    try:
        from sqlmodel import select

        statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        conversations = session.exec(statement).all()

        return [
            {
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            }
            for conv in conversations
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving conversations: {str(e)}"
        )


@router.get("/{user_id}/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    user_id: str,
    conversation_id: int,
    session: Session = Depends(get_session),
    user_data: AuthenticatedUser = Depends(require_auth)
):
    """
    Get all messages for a specific conversation

    Args:
        user_id: The ID of the user (should match the authenticated user)
        conversation_id: The ID of the conversation
        session: Database session
        user_data: Authenticated user data

    Returns:
        list: List of messages in the conversation
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Cannot access another user's conversations"
        )

    try:
        from sqlmodel import select

        # Verify the conversation belongs to the user
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        # Get messages for the conversation
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)
        messages = session.exec(statement).all()

        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving messages: {str(e)}"
        )


@router.delete("/{user_id}/conversations/{conversation_id}")
async def delete_conversation(
    user_id: str,
    conversation_id: int,
    session: Session = Depends(get_session),
    user_data: AuthenticatedUser = Depends(require_auth)
):
    """
    Delete a specific conversation

    Args:
        user_id: The ID of the user (should match the authenticated user)
        conversation_id: The ID of the conversation to delete
        session: Database session
        user_data: Authenticated user data

    Returns:
        dict: Confirmation of deletion
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Cannot access another user's conversations"
        )

    try:
        from sqlmodel import select

        # Verify the conversation belongs to the user
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        # Delete all messages in the conversation first
        statement = select(Message).where(Message.conversation_id == conversation_id)
        messages = session.exec(statement).all()
        for message in messages:
            session.delete(message)

        # Commit the message deletions before deleting the conversation
        session.commit()

        # Delete the conversation
        session.delete(conversation)
        session.commit()

        return {
            "message": "Conversation deleted successfully",
            "conversation_id": conversation_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting conversation: {str(e)}"
        )