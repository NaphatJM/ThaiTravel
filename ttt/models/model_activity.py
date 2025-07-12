from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

from .model_user import User


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    description: str
    location: str
    amount: float
    tax_return: float | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
