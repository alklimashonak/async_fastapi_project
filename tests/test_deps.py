import pytest
from fastapi import HTTPException
from httpx import AsyncClient

from app.api.dependencies import get_current_user
from app.core.security import create_access_token
from app.schemas.user import UserDB

pytestmark = pytest.mark.anyio


class TestGetCurrentUser:
    async def test_get_current_user_returns_user_correct_token(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        token = create_access_token(subject=test_user.email)

        user = await get_current_user(token=token)

        assert user.id == test_user.id

    async def test_get_current_user_raise_401_incorrect_token(
            self,
            async_client: AsyncClient,
            test_user: UserDB,
    ) -> None:
        token = create_access_token(subject='failed@email.com')

        with pytest.raises(HTTPException):
            await get_current_user(token=token)
