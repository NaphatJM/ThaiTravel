from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# from ttt.schemas import schema_user

if TYPE_CHECKING:
    from .model_activity import Activity


# class User(schema_user.User_schema, SQLModel, table=True):
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

    activities: list["Activity"] = Relationship(back_populates="user")
