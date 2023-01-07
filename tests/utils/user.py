import logging

from faker import Faker
from pydantic import EmailStr, SecretStr

from app.crud import crud_user
from app.schemas.user import UserDB, UserCreate

TEST_USER_EMAIL = 'testuser@mail.com'
TEST_USER_PASSWORD = '1234'

TEST_SUPERUSER_EMAIL = 'testadmin@mail.com'
TEST_SUPERUSER_PASSWORD = '1234'

logger = logging.getLogger(__name__)

fake = Faker()


async def create_test_user(
        email: EmailStr | None = None,
        password: SecretStr | None = None,
        is_superuser: bool | None = False,
) -> UserDB:
    email = email if email else fake.unique.email()
    password = password if password else fake.password()

    user_in = UserCreate(
        email=email,
        password=password,
    )

    return await crud_user.create(user_in=user_in, is_superuser=is_superuser)
