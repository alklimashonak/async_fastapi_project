import logging
import uuid

import pytest
from fastapi import HTTPException
from httpx import AsyncClient
from pydantic import EmailStr, SecretStr

from app.crud import crud_user
from app.schemas.user import UserDB, UserCreate, UserUpdate
from tests.utils.user import TEST_USER_PASSWORD

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.anyio


class TestGetUsers:
    async def test_get_users(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        users = await crud_user.get_users()

        assert len(users) == 1


class TestGetUserByID:
    async def test_get_user_by_existing_id_returns_user(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        user = await crud_user.get_user_by_id(user_id=test_user.id)

        assert user
        assert user.email == test_user.email

    async def test_get_user_by_wrong_id_returns_none(
            self,
            async_client: AsyncClient
    ) -> None:
        wrong_id = uuid.uuid4()
        user = await crud_user.get_user_by_id(user_id=wrong_id)

        assert not user


class TestGetUserByEmail:
    async def test_get_user_by_existing_email_returns_user(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        user = await crud_user.get_user_by_email(email=test_user.email)

        assert user
        assert user.email == test_user.email

    async def test_get_user_by_wrong_email_returns_none(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        wrong_email = 'qwe' + test_user.email
        user = await crud_user.get_user_by_email(email=wrong_email)

        assert not user


class TestCreateUser:
    async def test_create_user_works(
            self,
            async_client: AsyncClient
    ) -> None:
        user_data = UserCreate(
            email=EmailStr('newuser@mail.com'),
            password=SecretStr('1234'),
        )

        new_user = await crud_user.create(payload=user_data)

        assert new_user.email == user_data.email

    async def test_cant_create_user_if_email_already_exists(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        user_data = UserCreate(
            email=test_user.email,
            password=SecretStr('1234'),
        )

        with pytest.raises(HTTPException) as exc_info:
            await crud_user.create(payload=user_data)

        assert exc_info.value.status_code == 400
        assert 'already exists' in exc_info.value.detail


class TestAuthenticateUser:
    async def test_authentication_success(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        user = await crud_user.authenticate(
            email=test_user.email,
            password=SecretStr(TEST_USER_PASSWORD)
        )

        assert user
        assert user == test_user

    async def test_authentication_with_non_existed_email_failed(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        user = await crud_user.authenticate(
            email=test_user.email + 'qwe',
            password=SecretStr(TEST_USER_PASSWORD)
        )

        assert not user

    async def test_authentication_wrong_password_failed(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        user = await crud_user.authenticate(
            email=test_user.email,
            password=SecretStr(TEST_USER_PASSWORD + 'qwe')
        )

        assert not user


class TestUpdateUser:
    async def test_update_user_password_works(
            self,
            async_client: AsyncClient,
            test_user: UserDB
    ) -> None:
        new_password = SecretStr('12345678')
        update_data = UserUpdate(password=new_password)

        user = await crud_user.update(user_id=test_user.id, payload=update_data)
        authenticated_user = await crud_user.authenticate(email=test_user.email, password=new_password)

        assert user.id
        assert authenticated_user