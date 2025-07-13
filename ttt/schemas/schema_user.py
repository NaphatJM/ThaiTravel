# ttt/schemas/schema_user.py

from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    full_name: str
    citizen_id: str
    email: EmailStr
    phone: str
    address: str | None = None
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)


class User_create_schema(UserBase):
    password: str  # สำหรับสร้าง user ใหม่ต้องมี password


class User_update_schema(BaseModel):
    full_name: str | None = None
    citizen_id: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    is_admin: bool | None = None
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)


class User_schema(UserBase):  # ใช้เป็น response model ที่คืน id ด้วย
    id: int


# ----- เพิ่มสำหรับ auth -----


class UserRegisterSchema(User_create_schema):
    pass


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: int
