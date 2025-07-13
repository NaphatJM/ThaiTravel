from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# import bcrypt

if TYPE_CHECKING:
    from .model_activity import Activity


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


# class Login(BaseModel):
#     email: EmailStr
#     password: str


# class ChangedPassword(BaseModel):
#     current_password: str
#     new_password: str


# class ResetedPassword(BaseModel):
#     email: EmailStr
#     citizen_id: str


# class RegisteredUser(BaseUser):
#     password: str = pydantic.Field(json_schema_extra=dict(example="password"))


# class UpdatedUser(BaseUser):
#     roles: list[str]


# class Token(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str
#     expires_in: int
#     expires_at: datetime.datetime
#     scope: str
#     issued_at: datetime.datetime
#     user_id: int


# class ChangedPasswordUser(BaseModel):
#     current_password: str
#     new_password: str


# class DBUser(BaseUser, SQLModel, table=True):
#     __tablename__ = "users"
#     id: int | None = Field(default=None, primary_key=True)

#     password: str

#     register_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
#     updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
#     last_login_date: datetime.datetime | None = Field(default=None)

#     async def has_roles(self, roles):
#         for role in roles:
#             if role in self.roles:
#                 return True
#         return False

#     async def get_encrypted_password(self, plain_password):
#         return bcrypt.hashpw(
#             plain_password.encode("utf-8"), salt=bcrypt.gensalt()
#         ).decode("utf-8")

#     async def set_password(self, plain_password):
#         self.password = await self.get_encrypted_password(plain_password)

#     async def verify_password(self, plain_password):
#         return bcrypt.checkpw(
#             plain_password.encode("utf-8"), self.password.encode("utf-8")
#         )
