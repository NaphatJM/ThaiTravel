from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

# from ttt.schemas import schema_user


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    citizen_id: str
    email: str
    phone: str
    address: str
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
