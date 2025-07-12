from fastapi import APIRouter
from ttt.schemas.schema_user import User
from typing import List

router = APIRouter(prefix="/users", tags=["User"])

# Dummy in-memory storage for demonstration
users_db = [
    User(
        id=1,
        full_name="John Doe",
        citizen_id="1234567890123",
        email="john@example.com",
        phone="0812345678",
        address="123 Main St",
        is_admin=False,
    ),
    User(
        id=2,
        full_name="Jane Smith",
        citizen_id="9876543210987",
        email="jane@example.com",
        phone="0898765432",
        address="456 Second St",
        is_admin=False,
    ),
    User(
        id=3,
        full_name="Admin User",
        citizen_id="1112223334445",
        email="admin@example.com",
        phone="0812345678",
        address="789 Third St",
        is_admin=True,
    ),
]


@router.get("/")
async def get_users():
    return users_db


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    return {"error": "User not found"}


@router.post("/", response_model=User)
async def create_user(user: User):
    users_db.append(user)
    return user


@router.put("/{user_id}", response_model=User)
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
