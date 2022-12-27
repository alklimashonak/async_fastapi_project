from pydantic import BaseModel, EmailStr, SecretStr, UUID4


class UserBase(BaseModel):
    email: EmailStr | None


class UserDB(UserBase):
    id: UUID4
    hashed_password: str


class UserCreate(UserBase):
    email: EmailStr
    password: SecretStr


class UserResponse(BaseModel):
    user: UserBase
    access_token: str | None
    token_type: str | None = 'bearer'


class UserUpdate(BaseModel):
    password: SecretStr | None
