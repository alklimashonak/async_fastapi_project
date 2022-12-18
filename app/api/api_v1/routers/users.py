from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.crud import crud_user
from app.schemas.user import UserDB

router = APIRouter()


@router.get('/', response_model=list[UserDB])
async def get_users():
    return await crud_user.get_users()


@router.get('/me/', response_model=UserDB)
async def get_current_user(user: UserDB = Depends(get_current_user)):
    return user
