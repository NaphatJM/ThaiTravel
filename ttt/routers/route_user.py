from fastapi import APIRouter
from ttt.schemas.schema_user import User
from typing import List

router = APIRouter(prefix="/users", tags=["User"])

# Dummy in-memory storage for demonstration
users_db = [
    User(
        id=1,
        full_name="John Doe",
        thaiID="1234567890123",
        email="john@example.com",
        phone="0812345678",
        address="123 Main St",
        is_verified=True,
        is_admin=False,
        created_at="2024-01-01T00:00:00",
        updated_at="2024-01-01T00:00:00",
    ),
    User(
        id=2,
        full_name="Jane Doe",
        thaiID="9876543210987",
        email="jane@example.com",
        phone="0898765432",
        address="456 Second St",
        is_verified=False,
        is_admin=False,
        created_at="2024-01-02T00:00:00",
        updated_at="2024-01-02T00:00:00",
    ),
]


@router.get("/")
async def get_users():
    return users_db


@router.get("/{user_id}")
async def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    return {"error": "User not found"}


@router.post("/")
async def create_user(user: User):
    users_db.append(user)
    return user


@router.put("/{user_id}")
async def update_user(user_id: int, user: User):
    for idx, u in enumerate(users_db):
        if u.id == user_id:
            users_db[idx] = user
            return user
    return {"error": "User not found"}


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    for idx, user in enumerate(users_db):
        if user.id == user_id:
            users_db.pop(idx)
            return {"message": "User deleted", "user_id": user_id}
    return {"error": "User not found"}
