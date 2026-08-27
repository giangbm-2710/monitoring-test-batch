import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_category(client: AsyncClient):
    payload = {
        "name": "Electronics",
        "description": "Gadgets and tech items"
    }
    response = await client.post("/api/v1/categories/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert "id" in data

@pytest.mark.asyncio
async def test_create_duplicate_category(client: AsyncClient):
    payload = {"name": "Books", "description": "Reading material"}
    res1 = await client.post("/api/v1/categories/", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/api/v1/categories/", json=payload)
    assert res2.status_code == 400

@pytest.mark.asyncio
async def test_get_category_by_id(client: AsyncClient):
    create_res = await client.post("/api/v1/categories/", json={"name": "Clothing"})
    cat_id = create_res.json()["id"]

    response = await client.get(f"/api/v1/categories/{cat_id}")
    assert response.status_code == 200
    assert response.json()["id"] == cat_id
    assert response.json()["name"] == "Clothing"

@pytest.mark.asyncio
async def test_get_category_not_found(client: AsyncClient):
    response = await client.get("/api/v1/categories/99999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_categories(client: AsyncClient):
    for name in ["Cat 1", "Cat 2", "Cat 3"]:
        await client.post("/api/v1/categories/", json={"name": name})

    response = await client.get("/api/v1/categories/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 3

@pytest.mark.asyncio
async def test_update_category(client: AsyncClient):
    create_res = await client.post("/api/v1/categories/", json={"name": "Old Cat"})
    cat_id = create_res.json()["id"]

    update_res = await client.put(f"/api/v1/categories/{cat_id}", json={"name": "New Cat"})
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "New Cat"

@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient):
    create_res = await client.post("/api/v1/categories/", json={"name": "To Delete"})
    cat_id = create_res.json()["id"]

    del_res = await client.delete(f"/api/v1/categories/{cat_id}")
    assert del_res.status_code == 204

    get_res = await client.get(f"/api/v1/categories/{cat_id}")
    assert get_res.status_code == 404
