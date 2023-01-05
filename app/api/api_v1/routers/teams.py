from fastapi import Depends, APIRouter, HTTPException
from starlette import status

from app.api.dependencies import get_current_user
from app.crud import crud_team
from app.schemas.team import TeamResponse, TeamCreate, TeamUpdate
from app.schemas.user import UserDB

router = APIRouter()


@router.post('/', response_model=TeamResponse)
async def create_team(
        team_in: TeamCreate,
        current_user: UserDB = Depends(get_current_user),
) -> TeamResponse:
    user_teams = await crud_team.get_user_teams(user_id=current_user.id)

    if len(user_teams) > 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User can't have more than 3 teams")

    team = await crud_team.create(payload=team_in, owner_id=current_user.id)
    return TeamResponse(team=team)


@router.put('/{team_id}/', response_model=TeamResponse)
async def update_team(
        team_id: int,
        team_in: TeamUpdate,
        current_user: UserDB = Depends(get_current_user),
) -> TeamResponse:
    team_to_update = await crud_team.get_team_by_id(team_id=team_id)

    if team_to_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User can update only his own teams')

    new_team = await crud_team.update(team_id=team_id, payload=team_in)
    return TeamResponse(team=new_team)
