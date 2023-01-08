import logging

import pytest
from httpx import AsyncClient

from app.crud import crud_team, crud_driver
from app.schemas.team import TeamCreate, TeamUpdate
from app.schemas.user import UserDB
from tests.utils.driver import create_test_driver
from tests.utils.team import create_test_team
from tests.utils.user import create_test_user

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.anyio


class TestCreateTeam:
    async def test_create_team_works(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        drivers = [await create_test_driver() for _ in range(5)]
        drivers_ids = {driver.id for driver in drivers}

        team_in = TeamCreate(name='Test Team', picks=drivers_ids)

        new_team = await crud_team.create(team_in=team_in, owner_id=test_user.id)

        assert new_team.id
        assert new_team.name == team_in.name
        assert new_team.owner_id == test_user.id


class TestGetTeamByID:
    async def test_get_team_by_existing_id_returns_team(
            self,
            test_user: UserDB,
    ) -> None:
        test_team = await create_test_team(owner_id=test_user.id)

        team = await crud_team.get_team_by_id(team_id=test_team.id)

        assert team.id == test_team.id
        assert team.name == test_team.name

    async def test_get_team_by_non_existing_id_returns_none(
            self,
            test_user: UserDB,
    ) -> None:
        non_existing_id = 9192492
        team = await crud_team.get_team_by_id(team_id=non_existing_id)

        assert not team


class TestUpdateTeam:
    async def test_update_team_name_works(
            self,
            test_user: UserDB,
    ) -> None:
        update_data = TeamUpdate(name='New Team Name')

        test_team = await create_test_team(owner_id=test_user.id)

        updated_team = await crud_team.update(team_id=test_team.id, team_in=update_data)

        assert updated_team.name == update_data.name
        assert test_team.id == updated_team.id


class TestGetUserTeams:
    async def test_get_user_teams_works(self) -> None:
        user = await create_test_user()
        team1, team2 = await create_test_team(owner_id=user.id), await create_test_team(owner_id=user.id)

        user_teams = await crud_team.get_user_teams(user_id=user.id)

        assert len(user_teams) == 2
        assert team1 in user_teams and team2 in user_teams


class TestAddDriverToTeam:
    async def test_add_driver_works(self) -> None:
        user = await create_test_user()
        team = await create_test_team(owner_id=user.id)
        driver = await create_test_driver()

        await crud_team.add_driver(team_id=team.id, driver_id=driver.id)

        drivers = await crud_driver.get_team_drivers(team_id=team.id)

        assert len(drivers) == 6
        assert driver in drivers
