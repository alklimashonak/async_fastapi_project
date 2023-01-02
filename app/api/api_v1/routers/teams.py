from fastapi import Depends, APIRouter

from app.api.dependencies import get_current_user
from app.crud import crud_team
from app.schemas.team import TeamResponse, TeamCreate
from app.schemas.user import UserDB

router = APIRouter()


@router.post('/', response_model=TeamResponse)
async def create_team(
        team_in: TeamCreate,
        current_user: UserDB = Depends(get_current_user),
) -> TeamResponse:
    team = await crud_team.create(payload=team_in, owner_id=current_user.id)
    return TeamResponse(team=team)
