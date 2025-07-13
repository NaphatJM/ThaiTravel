from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
import bcrypt

if TYPE_CHECKING:
    from .model_activity import Activity


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    citizen_id: str
    email: str
    phone: str
    address: str
    is_admin: bool = False
    password: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_login_date: Optional[datetime] = None

    activities: list["Activity"] = Relationship(back_populates="user")

    # ----- Auth helper methods -----
    async def get_encrypted_password(self, plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

    async def set_password(self, plain_password: str):
        self.password = await self.get_encrypted_password(plain_password)

    async def verify_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), self.password.encode("utf-8")
        )
