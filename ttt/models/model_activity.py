from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from .model_user import User
    from .model_location import Province


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    description: str
    province_id: int = Field(foreign_key="province.id")
    amount: float
    tax_return: float | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="activities")
    province: "Province" = Relationship(back_populates="activities")
