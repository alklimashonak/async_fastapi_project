import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_example(async_client: AsyncClient):
    response = await async_client.get('/example/')

    assert response.status_code == 200
