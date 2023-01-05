import logging

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.crud import crud_user
from app.crud.crud_team import get_user_teams
from app.schemas.user import UserDB, UserWithTeamsResponse, UserForResponseWithTeams

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=list[UserDB])
async def get_users():
    return await crud_user.get_users()


@router.get('/me/', response_model=UserWithTeamsResponse)
async def get_current_user(user: UserDB = Depends(get_current_user)):
    user_teams = await get_user_teams(user_id=user.id)

    return UserWithTeamsResponse(
        user=UserForResponseWithTeams(
            **user.dict(),
            teams=user_teams
        ),
    )
