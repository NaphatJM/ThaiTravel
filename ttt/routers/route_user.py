from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from datetime import datetime
from ttt.schemas import schema_user
from ttt.models import model_user
from ttt import models

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users():
    statement = select(model_user.User)
    results = models.session.exec(statement)
    db_users = results.all()
    if not db_users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )
    return db_users


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int) -> model_user.User:
    db_user = models.session.get(model_user.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return db_user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: schema_user.User_create_schema) -> model_user.User:
    print(f"Creating user: {user.model_dump()}")
    db_user = model_user.User(**user.model_dump(exclude_unset=True))
    models.session.add(db_user)
    models.session.commit()
    models.session.refresh(db_user)
    return db_user


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int, user: schema_user.User_update_schema
) -> model_user.User:
    statement = select(model_user.User).where(model_user.User.id == user_id)
    results = models.session.exec(statement)
    db_user = results.one()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db_user.updated_at = datetime.now()
    models.session.add(db_user)
    models.session.commit()
    models.session.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    statement = select(model_user.User).where(model_user.User.id == user_id)
    results = models.session.exec(statement)
    db_user = results.one()
    models.session.delete(db_user)
    models.session.commit()
    return {"message": "User deleted", "user_id": user_id}
