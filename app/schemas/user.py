from pydantic import BaseModel, EmailStr, SecretStr, UUID4

from app.schemas.team import TeamDB


class UserBase(BaseModel):
    email: EmailStr | None = None
    is_superuser: bool = False


class BaseUserDB(UserBase):
    id: UUID4


class UserDB(BaseUserDB):
    hashed_password: str


class UserInResponse(BaseUserDB):
    pass


class UserResponse(BaseModel):
    user: UserInResponse


class UserWithTeamsResponse(UserResponse):
    teams: list[TeamDB]


class UserWithTokenResponse(UserResponse):
    access_token: str | None
    token_type: str | None = 'bearer'


class UserCreate(UserBase):
    email: EmailStr
    password: SecretStr


class UserUpdate(BaseModel):
    password: SecretStr | None
