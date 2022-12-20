import logging
import pathlib
from os import environ
from typing import AsyncGenerator

import pytest
from alembic import command
from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import EmailStr, SecretStr
from sqlalchemy_utils import database_exists, create_database, drop_database

environ["TESTING"] = "True"

from app.core.config import settings
from app.crud import crud_user
from app.schemas.user import UserDB, UserCreate

logger = logging.getLogger(__name__)

DROP_DATABASE_AFTER_TEST = False


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    root_dir = pathlib.Path(__file__).absolute().parent.parent
    ini_file = root_dir.joinpath("alembic.ini").__str__()
    alembic_directory = root_dir.joinpath("alembic").__str__()
    url = settings.DATABASE_URL
    if DROP_DATABASE_AFTER_TEST:
        assert not database_exists(url), "Test database already exists. Aborting tests."
    elif not database_exists(url):
        create_database(url)  # Create the test database.
    config = Config(ini_file)  # Run the migrations.
    config.set_main_option("script_location", alembic_directory)
    command.downgrade(config, "base")
    command.upgrade(config, "head")
    yield  # Run the tests.
    if DROP_DATABASE_AFTER_TEST:
        drop_database(url)


@pytest.fixture(scope='session')
async def app() -> FastAPI:
    from app.main import app
    return app


@pytest.fixture
async def test_user() -> UserDB:
    user_data = UserCreate(
        email=EmailStr('testuser@mail.com'),
        password=SecretStr('1234')
    )
    user_id = await crud_user.create(payload=user_data)

    return await crud_user.get_user_by_id(user_id=str(user_id))


@pytest.fixture
async def async_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app=app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
