from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.security import create_access_token
from app.crud import crud_user
from app.schemas.user import UserCreate, UserResponse, UserDB

router = APIRouter()


@router.post('/register/', response_model=UserResponse)
async def register(
        user_in: UserCreate
):
    user_id = await crud_user.create(payload=user_in)

    token = create_access_token(subject=str(user_id))
    return UserResponse(
        user=UserDB(**user_in.dict()),
        access_token=token,
    )


@router.post('/login/', response_model=UserResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud_user.authenticate(email=form_data.username, password=SecretStr(form_data.password))
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    token = create_access_token(subject=user.email)
    return UserResponse(
        user=UserDB(**user.dict()),
        access_token=token,
    )
