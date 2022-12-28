import pytest

from app.core.security import create_access_token, get_user_email_from_token

pytestmark = pytest.mark.anyio


async def test_create_access_token():
    test_subject = 'test@mail.com'
    test_expires_delta = None

    token = create_access_token(subject=test_subject, expires_delta=test_expires_delta)

    email = get_user_email_from_token(token=token)

    assert test_subject == email
