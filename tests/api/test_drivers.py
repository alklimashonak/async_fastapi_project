import pytest
from httpx import AsyncClient
from starlette import status

from app.core.security import create_access_token
from app.schemas.user import UserDB

pytestmark = pytest.mark.anyio


class TestCreateDriverAPI:
    async def test_user_cant_create_driver(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        token = create_access_token(subject=test_user.email)
        headers = {'Authorization': f'bearer {token}'}
        driver_data = {
            'first_name': 'Fernando',
            'last_name': 'Alonso',
            'short_name': 'ALO',
        }

        response = await async_client.post('/api/drivers/', json=driver_data, headers=headers)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()['detail'] == "The user doesn't have enough privileges"

    async def test_superuser_can_create_driver(
            self,
            async_client: AsyncClient,
            test_superuser: UserDB,
    ) -> None:
        token = create_access_token(subject=test_superuser.email)
        headers = {'Authorization': f'bearer {token}'}
        driver_data = {
            'first_name': 'Fernando',
            'last_name': 'Alonso',
            'short_name': 'ALO',
        }

        response = await async_client.post('/api/drivers/', json=driver_data, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['last_name'] == driver_data['last_name']
