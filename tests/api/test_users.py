import pytest
from httpx import AsyncClient

from app.core.security import create_access_token
from app.schemas.user import UserDB

pytestmark = pytest.mark.anyio


async def test_get_current_user_api_authorized_returns_user(
        async_client: AsyncClient,
        test_user: UserDB,
) -> None:
    token = create_access_token(subject=str(test_user.email))
    headers = {'Authorization': f'bearer {token}'}

    response = await async_client.get('/api/users/me/', headers=headers)

    assert response.status_code == 200
    assert response.json()['id'] == str(test_user.id)
    assert response.json()['email'] == test_user.email


async def test_get_current_user_api_unauthorized_raise_401(
        async_client: AsyncClient,
        test_user: UserDB,
) -> None:
    response = await async_client.get('/api/users/me/')

    assert response.status_code == 401
