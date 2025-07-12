from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):
    full_name: str
    citizen_id: str
    email: EmailStr
    phone: str
    address: str | None = None
    is_admin: bool = False
