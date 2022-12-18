from pydantic import BaseModel, EmailStr, SecretStr, UUID4


class UserBase(BaseModel):
    email: EmailStr | None


class UserDB(UserBase):
    id: UUID4
    hashed_password: str


class UserCreate(UserBase):
    email: EmailStr
    password: SecretStr


class UserWithToken(UserBase):
    token: str


class UserResponse(BaseModel):
    user: UserWithToken


class UserUpdate(UserBase):
    password: str | None
