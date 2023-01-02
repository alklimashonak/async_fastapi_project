from pydantic import BaseModel, EmailStr, SecretStr, UUID4


class UserBase(BaseModel):
    email: EmailStr | None = None
    is_superuser: bool = False


class User(UserBase):
    id: UUID4


class UserDB(User):
    hashed_password: str


class UserCreate(UserBase):
    email: EmailStr
    password: SecretStr


class UserUpdate(BaseModel):
    password: SecretStr | None


class UserResponse(BaseModel):
    user: User
    access_token: str | None
    token_type: str | None = 'bearer'
