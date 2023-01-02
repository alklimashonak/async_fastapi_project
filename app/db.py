import sqlalchemy
from databases import Database
from sqlalchemy import create_engine, MetaData, Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

metadata = MetaData()

database = Database(settings.DATABASE_URL, force_rollback=settings.TESTING)

users = sqlalchemy.Table(
    'users',
    metadata,
    Column('id', UUID, primary_key=True, index=True),
    Column('email', String(64), unique=True, index=True, nullable=False),
    Column('hashed_password', sqlalchemy.String),
    Column('is_superuser', Boolean, nullable=False, default=False)
)

teams = sqlalchemy.Table(
    'teams',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String(64), nullable=False),
    Column('owner_id', UUID, ForeignKey('users.id', ondelete='CASCADE'))
)
