from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class User_schema(BaseModel):
    full_name: str
    citizen_id: str
    email: EmailStr
    phone: str
    address: str | None = None
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)


class User_create_schema(User_schema):
    pass


class User_update_schema(User_schema):
    full_name: str | None = None
    citizen_id: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    is_admin: bool | None = None

    model_config = ConfigDict(from_attributes=True)
