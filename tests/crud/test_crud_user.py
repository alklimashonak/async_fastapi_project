import pytest
from httpx import AsyncClient

from app.crud import crud_user
from app.schemas.user import UserDB

pytestmark = pytest.mark.anyio


async def test_get_user_by_email(
        async_client: AsyncClient,
        test_user: UserDB,
) -> None:
    user = await crud_user.get_user_by_email(email=test_user.email)

    assert user
    assert user.email == test_user.email


async def test_get_users(
        async_client: AsyncClient
) -> None:
    users = await crud_user.get_users()

    assert len(users) == 0
