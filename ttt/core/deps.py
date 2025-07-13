from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

import jwt
from jwt import PyJWTError

from ttt.core import config, security
from ttt.models import DBUser, get_session
from sqlmodel.ext.asyncio.session import AsyncSession


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")  # หรือ /v1/token ถ้ามี prefix

settings = config.get_settings()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DBUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.ALGORITHM],
        )
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = await session.get(DBUser, user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[DBUser, Depends(get_current_user)],
) -> DBUser:
    # ปรับตาม status ถ้ามี
    return current_user


async def get_current_admin_user(
    current_user: Annotated[DBUser, Depends(get_current_user)],
) -> DBUser:
    if "admin" not in getattr(current_user, "roles", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have admin privileges",
        )
    return current_user
