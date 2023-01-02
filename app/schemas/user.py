from pydantic import BaseModel, EmailStr, SecretStr, UUID4


class UserBase(BaseModel):
    email: EmailStr | None


class UserDB(UserBase):
    id: UUID4
    email: EmailStr
    hashed_password: str
    is_superuser: bool


class UserCreate(UserBase):
    email: EmailStr
    password: SecretStr


class UserUpdate(BaseModel):
    password: SecretStr | None


class UserResponse(BaseModel):
    user: UserBase
    access_token: str | None
    token_type: str | None = 'bearer'
