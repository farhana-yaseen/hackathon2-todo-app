"""Push subscription models for Web Push notifications.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class PushSubscription(SQLModel, table=True):
    """Stores Web Push subscription details for a user."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    endpoint: str = Field(nullable=False, unique=True)
    p256dh: str = Field(nullable=False)
    auth: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    __tablename__ = "push_subscriptions"
