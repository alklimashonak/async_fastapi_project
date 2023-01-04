import pytest
from httpx import AsyncClient
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK

from app.core.security import create_access_token
from app.schemas.user import UserDB
from tests.utils.user import TEST_USER_EMAIL, TEST_USER_PASSWORD

pytestmark = pytest.mark.anyio


class TestGetCurrentUserAPI:
    async def test_get_current_user_api_authorized_returns_user(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        token = create_access_token(subject=str(test_user.email))
        headers = {'Authorization': f'bearer {token}'}

        response = await async_client.get('/api/users/me/', headers=headers)

        assert response.status_code == 200
        assert response.json()['user']['id'] == str(test_user.id)
        assert response.json()['user']['email'] == test_user.email

    async def test_get_current_user_api_unauthorized_raise_401(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        response = await async_client.get('/api/users/me/')

        assert response.status_code == HTTP_401_UNAUTHORIZED


class TestRegisterAPI:
    async def test_register_api_returns_user_info_with_token(
            self,
            async_client: AsyncClient
    ) -> None:
        email = 'testuser1@gmail.com'
        password = '1234'
        payload = {
            'email': email,
            'password': password,
        }

        response = await async_client.post('/api/auth/register/', json=payload)

        assert response.status_code == HTTP_200_OK
        assert response.json()['user']['email'] == email
        assert response.json()['access_token']


class TestLoginAPI:
    async def test_failed_login_raise_401(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        email = TEST_USER_EMAIL
        password = TEST_USER_PASSWORD + 'qwe'

        payload = {
            'username': email,
            'password': password,
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = await async_client.post('/api/auth/login/', headers=headers, data=payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED
