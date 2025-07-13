from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from ttt.schemas import schema_user


class User(schema_user.User_schema, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
