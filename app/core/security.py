from datetime import timedelta, datetime

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import SecretStr, ValidationError
from starlette import status

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/")

ALGORITHM = "HS256"


def create_access_token(
    subject: str, expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_email_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
        user_email = payload.get("sub", None)
        return user_email
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def verify_password(plain_password: SecretStr, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password.get_secret_value(), hashed_password)


def get_password_hash(password: SecretStr) -> str:
    return pwd_context.hash(password.get_secret_value())
