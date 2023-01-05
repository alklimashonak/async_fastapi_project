from pydantic import BaseModel, EmailStr, SecretStr, UUID4

from app.schemas.team import TeamForUserResponse


class UserBase(BaseModel):
    email: EmailStr | None = None


class BaseUserDB(UserBase):
    id: UUID4
    is_superuser: bool = False


class UserDB(BaseUserDB):
    hashed_password: str


class UserForResponse(BaseUserDB):
    pass


class UserForResponseWithTeams(BaseUserDB):
    teams: list[TeamForUserResponse]


class UserResponse(BaseModel):
    user: UserForResponse


class UserWithTeamsResponse(UserResponse):
    user: UserForResponseWithTeams


class UserWithTokenResponse(UserResponse):
    access_token: str | None
    token_type: str | None = 'bearer'


class UserCreate(UserBase):
    email: EmailStr
    password: SecretStr


class UserUpdate(BaseModel):
    password: SecretStr | None
