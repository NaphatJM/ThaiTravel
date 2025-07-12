from fastapi import APIRouter
from ttt.schemas.schema_user import User_schema
from ttt.models import model_user
from sqlmodel import Session
from ttt.models import engine


router = APIRouter(prefix="/users", tags=["User"])


@router.get("/")
async def get_users():
    return [
        {
            "id": 1,
            "full_name": "John Doe",
            "thaiID": "1234567890123",
            "email": "john@example.com",
            "phone": "0812345678",
            "address": "123 Main St",
            "is_verified": True,
            "is_admin": False,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        },
        {
            "id": 2,
            "full_name": "Jane Smith",
            "thaiID": "9876543210987",
            "email": "jane@example.com",
            "phone": "0823456789",
            "address": "456 Elm St",
            "is_verified": False,
            "is_admin": True,
            "created_at": "2024-01-02T00:00:00",
            "updated_at": "2024-01-02T00:00:00",
        },
    ]


@router.get("/{user_id}")
async def get_user(user_id: int) -> User_schema:
    return {
        "id": 1,
        "full_name": "John Doe",
        "thaiID": "1234567890123",
        "email": "john@example.com",
        "phone": "0812345678",
        "address": "123 Main St",
        "is_verified": True,
        "is_admin": False,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }


@router.post("/")
async def create_user(user: User_schema) -> model_user.User:
    print(f"Creating user: {user.model_dump()}")
    db_user = model_user.User(**user.model_dump(exclude_unset=True))
    with Session(engine) as session:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return user


@router.put("/{user_id}")
async def update_user(user_id: int, user: User_schema) -> dict:
    return {"message": user, "user_id": user_id}


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    return {"message": "User deleted", "user_id": user_id}
