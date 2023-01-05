import string
import random

from pydantic import UUID4

from app.crud import crud_team
from app.schemas.team import TeamDB, TeamCreate


def get_random_string(length=8):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


async def create_test_team(
        owner_id: UUID4,
        team_name: str | None = None,
) -> TeamDB:
    if team_name:
        team_data = TeamCreate(name=team_name)
    else:
        team_data = TeamCreate(name=get_random_string())

    return await crud_team.create(team_in=team_data, owner_id=owner_id)
