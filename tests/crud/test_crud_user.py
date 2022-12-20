import pytest
from httpx import AsyncClient
from pydantic import EmailStr, SecretStr

from app.crud import crud_user
from app.schemas.user import UserDB, UserCreate

pytestmark = pytest.mark.anyio


async def test_get_user_by_id(
        async_client: AsyncClient,
        test_user: UserDB,
) -> None:
    user = await crud_user.get_user_by_id(user_id=test_user.id)

    assert user
    assert user.email == test_user.email


async def test_get_user_by_email(
        async_client: AsyncClient,
        test_user: UserDB,
) -> None:
    user = await crud_user.get_user_by_email(email=test_user.email)

    assert user
    assert user.email == test_user.email


async def test_get_users(
        async_client: AsyncClient
) -> None:
    users = await crud_user.get_users()

    assert len(users) == 0


async def test_create_user(
        async_client: AsyncClient
) -> None:
    user_data = UserCreate(
        email=EmailStr('newuser@mail.com'),
        password=SecretStr('1234'),
    )
    users_before = await crud_user.get_users()
    new_user_id = await crud_user.create(payload=user_data)
    new_user = await crud_user.get_user_by_id(user_id=new_user_id)
    users_after = await crud_user.get_users()

    assert len(users_before) == 0
    assert len(users_after) == 1
    assert new_user.email == user_data.email


async def test_authenticate_user(
        async_client: AsyncClient,
        test_user: UserDB,
) -> None:
    user = await crud_user.authenticate(
        email=test_user.email,
        password=SecretStr('1234')
    )

    assert user == test_user
