import pytest
from httpx import AsyncClient
from pydantic import EmailStr, SecretStr

from app.crud import crud_user
from app.schemas.user import UserDB, UserCreate, UserUpdate
from tests.utils.user import TEST_USER_PASSWORD

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
        async_client: AsyncClient,
        test_user: UserDB,
) -> None:
    users = await crud_user.get_users()

    assert len(users) == 1


async def test_create_user(
        async_client: AsyncClient
) -> None:
    user_data = UserCreate(
        email=EmailStr('newuser@mail.com'),
        password=SecretStr('1234'),
    )
    users_before = await crud_user.get_users()
    new_user = await crud_user.create(payload=user_data)
    users_after = await crud_user.get_users()

    assert len(users_before) == 0
    assert len(users_after) == 1
    assert new_user.email == user_data.email


async def test_update_user_password(
        async_client: AsyncClient,
        test_user: UserDB
) -> None:
    new_password = SecretStr('12345678')
    update_data = UserUpdate(password=new_password)

    user = await crud_user.update(user_id=test_user.id, payload=update_data)
    authenticated_user = await crud_user.authenticate(email=test_user.email, password=new_password)

    assert user.id
    assert authenticated_user


async def test_authentication_success(
        async_client: AsyncClient,
        test_user: UserDB,
) -> None:
    user = await crud_user.authenticate(
        email=test_user.email,
        password=SecretStr(TEST_USER_PASSWORD)
    )

    users = await crud_user.get_users()

    assert len(users) == 1

    assert user
    assert user == test_user


async def test_authentication_with_non_existed_email(
        async_client: AsyncClient,
        test_user: UserDB,
) -> None:
    user = await crud_user.authenticate(
        email=test_user.email + 'qwe',
        password=SecretStr(TEST_USER_PASSWORD)
    )

    assert not user


async def test_authentication_wrong_password(
        async_client: AsyncClient,
        test_user: UserDB,
) -> None:
    user = await crud_user.authenticate(
        email=test_user.email,
        password=SecretStr(TEST_USER_PASSWORD + 'qwe')
    )

    assert not user
