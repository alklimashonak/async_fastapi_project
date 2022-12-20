import logging
import uuid

from fastapi import HTTPException
from pydantic import UUID4, SecretStr
from starlette.status import HTTP_400_BAD_REQUEST

from app import db
from app.core.security import get_password_hash, verify_password
from app.db import database
from app.schemas.user import UserCreate, UserDB

logger = logging.getLogger(__name__)


async def create(payload: UserCreate) -> UUID4 | None:
    user_db = await get_user_by_email(email=payload.email)
    if user_db:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    query = db.users.insert().values(
        id=uuid.uuid4(),
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
    ).returning(db.users.c.id)
    return await database.execute(query=query)


async def get_user_by_email(email: str) -> UserDB | None:
    query = db.users.select().where(email == db.users.c.email)
    user_row = await database.fetch_one(query=query)
    return UserDB(**user_row) if user_row else None


async def get_user_by_id(user_id: str) -> UserDB | None:
    query = db.users.select().where(user_id == db.users.c.id)
    user_row = await database.fetch_one(query=query)
    return UserDB(**user_row) if user_row else None


async def get_users() -> list[UserDB]:
    query = db.users.select()

    users = await database.fetch_all(query=query)
    return [UserDB(**user) for user in users]


async def authenticate(email: str, password: SecretStr) -> UserDB | None:
    user_db = await get_user_by_email(email=email)
    if not user_db:
        return None
    if not verify_password(password, user_db.hashed_password):
        return None
    return user_db
