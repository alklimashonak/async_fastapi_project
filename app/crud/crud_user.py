import logging
import uuid

from pydantic import UUID4, SecretStr

from app import db
from app.core.security import get_password_hash, verify_password
from app.db import database
from app.schemas.user import UserCreate, UserDB, UserUpdate

logger = logging.getLogger(__name__)


async def create(user_in: UserCreate) -> UserDB | None:
    query = db.users.insert() \
        .values(
            id=uuid.uuid4(),
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
        ) \
        .returning(db.users.c.id, db.users.c.email, db.users.c.hashed_password, db.users.c.is_superuser)

    user_row = await database.fetch_one(query=query)
    return UserDB(**user_row._mapping) if user_row else None


async def get_user_by_email(email: str) -> UserDB | None:
    query = db.users.select().where(email == db.users.c.email)
    user_row = await database.fetch_one(query=query)
    return UserDB(**user_row._mapping) if user_row else None


async def get_user_by_id(user_id: UUID4) -> UserDB | None:
    query = db.users.select().where(user_id == db.users.c.id)
    user_row = await database.fetch_one(query=query)
    return UserDB(**user_row._mapping) if user_row else None


async def get_users() -> list[UserDB]:
    query = db.users.select()

    users = await database.fetch_all(query=query)
    return [UserDB(**user._mapping) for user in users]


async def update(user_id: UUID4, user_in: UserUpdate) -> UserDB | None:
    new_hashed_password = get_password_hash(password=user_in.password)

    query = db.users.update() \
        .where(db.users.c.id == user_id) \
        .values(hashed_password=new_hashed_password) \
        .returning(db.users.c.id, db.users.c.email, db.users.c.hashed_password, db.users.c.is_superuser)

    user_row = await database.fetch_one(query=query)
    return UserDB(**user_row._mapping) if user_row else None


async def authenticate(email: str, password: SecretStr) -> UserDB | None:
    user_db = await get_user_by_email(email=email)
    if not user_db:
        return None
    if not verify_password(password, user_db.hashed_password):
        return None
    return user_db
