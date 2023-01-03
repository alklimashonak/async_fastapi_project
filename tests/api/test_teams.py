import pytest
from httpx import AsyncClient
from pydantic import EmailStr, SecretStr
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_403_FORBIDDEN

from app.core.security import create_access_token
from app.crud import crud_user
from app.schemas.user import UserDB, UserCreate
from tests.utils.team import create_test_team

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


class TestUpdateTeamAPI:
    async def test_user_can_update_his_own_team(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        team = await create_test_team(owner_id=test_user.id)
        token = create_access_token(subject=test_user.email)

        payload = {
            'name': 'Updated Team'
        }

        headers = {
            'Authorization': f'bearer {token}'
        }

        response = await async_client.put(f'/api/teams/{team.id}/', json=payload, headers=headers)

        assert response.status_code == HTTP_200_OK
        assert response.json()['team']['name'] == payload.get('name')

    async def test_user_cant_update_not_his_own_team(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        user_in = UserCreate(
            email=EmailStr('someuser@example.com'),
            password=SecretStr('1234')
        )

        team_payload = {
            'name': 'New Team Name'
        }

        user = await crud_user.create(payload=user_in)
        team = await create_test_team(owner_id=test_user.id)
        token = create_access_token(subject=user.email)

        headers = {
            'Authorization': f'bearer {token}'
        }

        response = await async_client.put(f'/api/teams/{team.id}/', json=team_payload, headers=headers)

        assert response.status_code == HTTP_403_FORBIDDEN
