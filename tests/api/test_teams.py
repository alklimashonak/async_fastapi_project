import pytest
from httpx import AsyncClient
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK

from app.core.security import create_access_token
from app.schemas.user import UserDB

pytestmark = pytest.mark.anyio


class TestCreateTeamAPI:
    async def test_logged_user_can_create_team(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        team_data = {
            'name': 'New Team'
        }
        token = create_access_token(subject=test_user.email)
        headers = {
            'Authorization': f'bearer {token}'
        }

        response = await async_client.post('/api/teams/', json=team_data, headers=headers)

        assert response.status_code == HTTP_200_OK
        assert response.json()['team']['id']
        assert response.json()['team']['name'] == team_data.get('name')
        assert response.json()['team']['owner_id'] == str(test_user.id)

    async def test_not_logged_user_cant_create_team(
            self,
            async_client: AsyncClient,
            test_user: UserDB
    ) -> None:
        team_data = {
            'name': 'New Team 2'
        }

        response = await async_client.post('/api/teams/', json=team_data)

        assert response.status_code == HTTP_401_UNAUTHORIZED
