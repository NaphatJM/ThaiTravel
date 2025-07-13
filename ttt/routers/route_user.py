from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlmodel import select
from datetime import datetime
from ttt.schemas import schema_user
from ttt.models import model_user
from ttt import models

router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[schema_user.User_schema]
)
async def get_users(session: AsyncSession = Depends(models.get_session)):
    statement = select(model_user.User)
    results = await session.exec(statement)
    db_users = results.all()
    if not db_users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )
    return [schema_user.User_schema.model_validate(u) for u in db_users]


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=schema_user.User_schema
)
async def get_user(
    user_id: int, session: AsyncSession = Depends(models.get_session)
) -> model_user.User:
    db_user = await session.get(model_user.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return schema_user.User_schema.model_validate(db_user)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schema_user.User_schema
)
async def create_user(
    user: schema_user.User_create_schema,
    session: AsyncSession = Depends(models.get_session),
) -> model_user.User:
    db_user = model_user.User(**user.model_dump(exclude_unset=True))
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return schema_user.User_schema.model_validate(db_user)


@router.put(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=schema_user.User_schema
)
async def update_user(
    user_id: int,
    user: schema_user.User_update_schema,
    session: AsyncSession = Depends(models.get_session),
) -> model_user.User:
    statement = select(model_user.User).where(model_user.User.id == user_id)
    results = await session.exec(statement)
    db_user = results.one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db_user.updated_at = datetime.now()
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return schema_user.User_schema.model_validate(db_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, session: AsyncSession = Depends(models.get_session)
):
    statement = select(model_user.User).where(model_user.User.id == user_id)
    results = await session.exec(statement)
    db_user = results.one_or_none()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    await session.delete(db_user)
    await session.commit()
    return {"message": "User deleted", "user_id": user_id}
