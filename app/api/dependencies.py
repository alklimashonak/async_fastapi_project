from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.config import settings
from app.core.security import oauth2_scheme, ALGORITHM
from app.crud.crud_user import get_user_by_email
from app.schemas.user import UserDB


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> UserDB:
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(email=email)
    if not user:
        raise credentials_exception
    return user


async def get_current_superuser(
        current_user: UserDB = Depends(get_current_user),
) -> UserDB:
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user doesn't have enough privileges")
    return current_user
