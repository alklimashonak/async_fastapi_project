import os

import pytest

from app.core.config import Settings

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    'testing,url',
    [
        ('FALSE', 'postgresql://postgres:postgres@localhost/example'),
        ('TRUE', 'postgresql://postgres:postgres@localhost/test_example'),
    ],
)
async def test_postgres_config(testing: str, url: str):
    if os.environ.get('SQLALCHEMY_DATABASE_URI'):
        os.environ.pop('SQLALCHEMY_DATABASE_URI')
    os.environ['POSTGRES_SERVER'] = 'localhost'
    os.environ['POSTGRES_USER'] = 'postgres'
    os.environ['POSTGRES_PASSWORD'] = 'postgres'
    os.environ['POSTGRES_DB'] = 'example'
    os.environ['TESTING'] = testing

    settings = Settings()
    assert isinstance(settings.DATABASE_URL, str)
    assert settings.DATABASE_URL == url
