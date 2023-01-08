import pytest
from httpx import AsyncClient
from pydantic import EmailStr, SecretStr
from starlette import status

from app.core.security import create_access_token
from app.crud import crud_user
from app.schemas.user import UserDB, UserCreate
from tests.utils.driver import create_test_driver
from tests.utils.team import create_test_team
from tests.utils.user import create_test_user

pytestmark = pytest.mark.anyio


class TestGetTeamAPI:
    async def test_get_team_by_id_works(
            self,
            async_client: AsyncClient,
    ) -> None:
        user = await create_test_user()
        team = await create_test_team(owner_id=user.id)

        response = await async_client.get(f'/api/teams/{team.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['team']['name'] == team.name


class TestCreateTeamAPI:
    async def test_logged_user_can_create_team(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        drivers = [await create_test_driver() for _ in range(5)]
        drivers_ids = [driver.id for driver in drivers]

        team_data = {
            'name': 'Team One',
            'picks': drivers_ids,
        }
        token = create_access_token(subject=test_user.email)
        headers = {
            'Authorization': f'bearer {token}'
        }

        response = await async_client.post('/api/teams/', json=team_data, headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['team']['id']
        assert response.json()['team']['name'] == team_data.get('name')
        assert response.json()['team']['owner_id'] == str(test_user.id)

    async def test_not_logged_user_cant_create_team(
            self,
            async_client: AsyncClient,
            test_user: UserDB
    ) -> None:
        team_data = {
            'name': 'Team Two'
        }

        response = await async_client.post('/api/teams/', json=team_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_user_cant_create_team_if_already_has_3(
            self,
            async_client: AsyncClient,
    ) -> None:
        user_data = UserCreate(email=EmailStr('testuser1@example.com'), password=SecretStr('1234'))
        user = await crud_user.create(user_in=user_data)
        token = create_access_token(subject=user.email)
        headers = {
            'Authorization': f'bearer {token}'
        }

        drivers = [await create_test_driver() for _ in range(5)]
        drivers_ids = [driver.id for driver in drivers]

        await create_test_team(owner_id=user.id)
        await create_test_team(owner_id=user.id)
        await create_test_team(owner_id=user.id)

        team_in = {
            'name': 'Team Three',
            'picks': drivers_ids,
        }

        response = await async_client.post('/api/teams/', json=team_in, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()['detail'] == "User can't have more than 3 teams"


class TestUpdateTeamAPI:
    async def test_user_can_update_his_own_team(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        team = await create_test_team(owner_id=test_user.id, team_name='Team Three')
        token = create_access_token(subject=test_user.email)

        payload = {
            'name': 'Team Three Updated'
        }

        headers = {
            'Authorization': f'bearer {token}'
        }

        response = await async_client.put(f'/api/teams/{team.id}/', json=payload, headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['team']['name'] == payload.get('name')

    async def test_user_cant_update_not_his_own_team(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        user_in = UserCreate(
            email=EmailStr('testuser2@example.com'),
            password=SecretStr('1234')
        )

        team_payload = {
            'name': 'Team Four Updated'
        }

        user = await crud_user.create(user_in=user_in)
        team = await create_test_team(owner_id=test_user.id, team_name='Team Four')
        token = create_access_token(subject=user.email)

        headers = {
            'Authorization': f'bearer {token}'
        }

        response = await async_client.put(f'/api/teams/{team.id}/', json=team_payload, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(
        'user_email, team_name, status_code',
        [
            ('newuser1@example.com', 'Team Five Updated', 200),
            ('newuser2@example.com', 'TeamFive'*10, 422)
        ]
    )
    async def test_update_team_validation(
            self,
            async_client: AsyncClient,
            user_email: str,
            team_name: str,
            status_code: int
    ) -> None:
        user_in = UserCreate(
            email=EmailStr(user_email),
            password=SecretStr('1234')
        )

        team_payload = {
            'name': team_name
        }

        user = await crud_user.create(user_in=user_in)
        team = await create_test_team(owner_id=user.id, team_name='Team Five')
        token = create_access_token(subject=user.email)

        headers = {
            'Authorization': f'bearer {token}'
        }

        response = await async_client.put(f'/api/teams/{team.id}/', json=team_payload, headers=headers)

        assert response.status_code == status_code
