import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_users_empty(client: AsyncClient):
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_nonexistent_user(client: AsyncClient):
    response = await client.get("/api/v1/users/999")
    assert response.status_code == 404
