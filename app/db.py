import sqlalchemy
from databases import Database
from sqlalchemy import create_engine, MetaData, Column, String, Integer, ForeignKey, Boolean, false
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
    Column('is_superuser', Boolean, nullable=False, server_default=false()),
)

teams = sqlalchemy.Table(
    'teams',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String(64), nullable=False),
    Column('owner_id', UUID, ForeignKey('users.id', ondelete='CASCADE')),
)


drivers = sqlalchemy.Table(
    'drivers',
    metadata,
    sqlalchemy.Column('id', Integer, primary_key=True),
    sqlalchemy.Column('first_name', sqlalchemy.String(64), nullable=False),
    sqlalchemy.Column('last_name', sqlalchemy.String(64), nullable=False),
    sqlalchemy.Column('short_name', sqlalchemy.String(5), nullable=False),
)

drivers_teams = sqlalchemy.Table(
    'drivers_teams',
    metadata,
    sqlalchemy.Column('driver_id', sqlalchemy.ForeignKey('drivers.id', ondelete='CASCADE')),
    sqlalchemy.Column('team_id', sqlalchemy.ForeignKey('teams.id', ondelete='CASCADE')),
)
