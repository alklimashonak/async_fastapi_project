import logging

from fastapi import Depends, APIRouter, HTTPException
from starlette import status

from app.api.dependencies import get_current_user
from app.crud import crud_team, crud_driver
from app.schemas.driver import DriverForTeamResponse, DriverDB
from app.schemas.team import TeamResponse, TeamCreate, TeamUpdate, TeamForResponse
from app.schemas.user import UserDB

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/{team_id}/', response_model=TeamResponse)
async def get_team(
        team_id: int,
) -> TeamResponse:
    team = await crud_team.get_team_by_id(team_id=team_id)
    drivers = await crud_driver.get_team_drivers(team_id=team_id)
    return TeamResponse(
        team=TeamForResponse(
            id=team.id,
            name=team.name,
            owner_id=team.owner_id,
            drivers=gen_drivers_for_team_response(drivers=drivers),
        )
    )


@router.post('/', response_model=TeamResponse)
async def create_team(
        team_in: TeamCreate,
        current_user: UserDB = Depends(get_current_user),
) -> TeamResponse:
    user_teams = await crud_team.get_user_teams(user_id=current_user.id)
    drivers = await crud_driver.get_drivers_by_ids(drivers_ids=list(team_in.picks))
    if len(user_teams) > 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User can't have more than 3 teams")
    if len(drivers) != 5:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Driver you picked does not exist')

    team = await crud_team.create(team_in=team_in, owner_id=current_user.id)

    return TeamResponse(
        team=TeamForResponse(
            id=team.id,
            name=team.name,
            owner_id=team.owner_id,
            drivers=gen_drivers_for_team_response(drivers=drivers),
        )
    )


@router.put('/{team_id}/', response_model=TeamResponse)
async def update_team(
        team_id: int,
        team_in: TeamUpdate,
        current_user: UserDB = Depends(get_current_user),
) -> TeamResponse:
    team_to_update = await crud_team.get_team_by_id(team_id=team_id)

    drivers = await crud_driver.get_team_drivers(team_id=team_id)

    if team_to_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User can update only his own teams')

    new_team = await crud_team.update(team_id=team_id, team_in=team_in)
    return TeamResponse(
        team=TeamForResponse(
            id=new_team.id,
            name=new_team.name,
            owner_id=new_team.owner_id,
            drivers=gen_drivers_for_team_response(drivers=drivers)
        )
    )


def gen_drivers_for_team_response(drivers: list[DriverDB]) -> list[DriverForTeamResponse]:
    return [DriverForTeamResponse(**driver.dict()) for driver in drivers]
