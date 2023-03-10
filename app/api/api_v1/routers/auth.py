from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from starlette import status

from app.core.security import create_access_token
from app.crud import crud_user
from app.schemas.user import UserCreate, UserWithTokenResponse, UserForResponse

router = APIRouter()


@router.post('/register/', response_model=UserWithTokenResponse)
async def register(
        user_in: UserCreate
):
    user = await crud_user.get_user_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    user = await crud_user.create(user_in=user_in)

    token = create_access_token(subject=str(user.id))
    return UserWithTokenResponse(
        user=UserForResponse(**user.dict()),
        access_token=token,
    )


@router.post('/login/', response_model=UserWithTokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud_user.authenticate(email=form_data.username, password=SecretStr(form_data.password))
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    token = create_access_token(subject=user.email)
    return UserWithTokenResponse(
        user=UserForResponse(**user.dict()),
        access_token=token,
    )
