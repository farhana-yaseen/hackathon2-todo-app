"""Notification API routes for Web Push notifications.
"""
import json
import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlmodel import select, and_
from pywebpush import webpush, WebPushException

from models import PushSubscription, Task
from db import AuthenticatedUser, require_auth, get_session

# Router configuration
router = APIRouter(prefix="/api/notifications", tags=["notifications"])
logger = logging.getLogger(__name__)

# VAPID Configuration
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_SUBJECT = os.getenv("VAPID_SUBJECT", "mailto:admin@example.com")

# ========== Pydantic Models ==========

class PushSubscriptionCreate(BaseModel):
    """Request model for saving a push subscription."""
    endpoint: str
    keys: dict

class TaskNotification(BaseModel):
    """Model for task notification data sent to client."""
    id: int
    title: str
    due_date: Optional[datetime]

class SuccessResponse(BaseModel):
    """Generic success response."""
    success: bool
    message: str

# ========== Helper Functions ==========

def send_push_notification(subscription: PushSubscription, data: dict):
    """Sends a push notification using pywebpush."""
    if not VAPID_PRIVATE_KEY or not VAPID_PUBLIC_KEY:
        logger.error("VAPID keys not configured. Cannot send notification.")
        return False

    try:
        webpush(
            subscription_info={
                "endpoint": subscription.endpoint,
                "keys": {
                    "p256dh": subscription.p256dh,
                    "auth": subscription.auth
                }
            },
            data=json.dumps(data),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": VAPID_SUBJECT}
        )
        return True
    except WebPushException as ex:
        logger.error(f"WebPush error: {ex}")
        # If the endpoint is no longer valid, we should ideally delete it
        if ex.response and ex.response.status_code in [404, 410]:
            logger.info(f"Removing invalid subscription: {subscription.endpoint}")
            return "REMOVE"
        return False
    except Exception as ex:
        logger.error(f"Unexpected push error: {ex}")
        return False

# ========== Endpoints ==========

@router.post("/subscribe", response_model=SuccessResponse)
async def subscribe(
    sub_data: PushSubscriptionCreate,
    user: AuthenticatedUser = Depends(require_auth),
    session: Session = Depends(get_session)
):
    """Saves or updates a user's push subscription."""
    # Check if subscription already exists
    existing = session.exec(
        select(PushSubscription).where(PushSubscription.endpoint == sub_data.endpoint)
    ).first()

    if existing:
        existing.user_id = user.user_id
        existing.p256dh = sub_data.keys.get("p256dh")
        existing.auth = sub_data.keys.get("auth")
    else:
        new_sub = PushSubscription(
            user_id=user.user_id,
            endpoint=sub_data.endpoint,
            p256dh=sub_data.keys.get("p256dh"),
            auth=sub_data.keys.get("auth")
        )
        session.add(new_sub)

    session.commit()
    return SuccessResponse(success=True, message="Subscription saved successfully")

@router.post("/process", response_model=SuccessResponse)
async def process_reminders(
    session: Session = Depends(get_session)
):
    """Processes pending task reminders and sends push notifications.

    This endpoint should be called periodically by a CRON job.
    """
    now = datetime.utcnow()
    # Find tasks due within the next 15 minutes that haven't been reminded yet
    window = now + timedelta(minutes=15)

    query = select(Task).where(
        and_(
            Task.reminder_enabled == True,
            Task.completed == False,
            Task.due_date <= window,
            Task.due_date >= now - timedelta(hours=1), # Don't remind for very old tasks
            Task.last_reminded_at == None
        )
    )

    tasks_to_notify = session.exec(query).all()
    count = 0

    for task in tasks_to_notify:
        # Get all subscriptions for this user
        subs = session.exec(
            select(PushSubscription).where(PushSubscription.user_id == task.user_id)
        ).all()

        if not subs:
            continue

        notification_data = {
            "title": "Task Reminder",
            "body": f"Your task '{task.title}' is due soon!",
            "data": {
                "taskId": task.id,
                "url": "/" # Could link directly to task
            }
        }

        sent_any = False
        to_remove = []

        for sub in subs:
            result = send_push_notification(sub, notification_data)
            if result == "REMOVE":
                to_remove.append(sub)
            elif result:
                sent_any = True

        # Cleanup invalid subs
        for sub in to_remove:
            session.delete(sub)

        if sent_any:
            task.last_reminded_at = now
            count += 1

    session.commit()
    return SuccessResponse(success=True, message=f"Processed {len(tasks_to_notify)} tasks, sent {count} notifications")

@router.post("/test", response_model=SuccessResponse)
async def test_notification(
    user: AuthenticatedUser = Depends(require_auth),
    session: Session = Depends(get_session)
):
    """Sends a test notification to the current user's active subscriptions."""
    subs = session.exec(
        select(PushSubscription).where(PushSubscription.user_id == user.user_id)
    ).all()

    if not subs:
        raise HTTPException(status_code=400, detail="No active push subscriptions found for user")

    notification_data = {
        "title": "Test Notification",
        "body": "This is a test notification from your Todo App!",
        "data": {"url": "/"}
    }

    sent_count = 0
    for sub in subs:
        if send_push_notification(sub, notification_data):
            sent_count += 1

    return SuccessResponse(success=True, message=f"Test notification sent to {sent_count} device(s)")
