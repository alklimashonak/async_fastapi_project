import logging

import pytest
from httpx import AsyncClient

from app.crud import crud_team
from app.schemas.team import TeamCreate
from app.schemas.user import UserDB

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.anyio


class TestCreateTeam:
    async def test_create_team_works(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ):
        team_data = TeamCreate(name='Test Team')

        new_team = await crud_team.create(payload=team_data, owner_id=test_user.id)

        assert new_team.id
        assert new_team.name == team_data.name
        assert new_team.owner_id == test_user.id


class TestGetTeamByID:
    pass
