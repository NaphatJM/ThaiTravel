from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from datetime import datetime, timedelta

from ttt.schemas.schema_user import TokenSchema
from ttt.schemas.schema_user import UserRegisterSchema
from ttt.models.model_user import User
from ttt.core.security import create_access_token, verify_password, get_password_hash
from ttt.models import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from ttt.core.config import get_settings

router = APIRouter(tags=["Authentication"])
settings = get_settings()


@router.post("/token", response_model=TokenSchema)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    # Allow login by email
    query = select(User).where(User.email == form_data.username)
    result = await session.exec(query)
    user = result.one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return TokenSchema(
        access_token=access_token,
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        user_id=user.id,
    )


@router.post("/register", response_model=dict)
async def register_user(
    user_data: UserRegisterSchema,
    session: AsyncSession = Depends(get_session),
):
    # Check if user with same email exists
    existing = await session.exec(select(User).where(User.email == user_data.email))
    if existing.one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = get_password_hash(user_data.password)

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        citizen_id=user_data.citizen_id,
        phone=user_data.phone,
        address=user_data.address,
        is_admin=False,
        password=hashed_pwd,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}
