import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

@pytest.mark.asyncio
async def test_create_product(client: AsyncClient):
    payload = {
        "name": "Test Laptop",
        "description": "Powerful machine",
        "price": 999.99,
        "stock": 10,
        "category": "Electronics"
    }
    response = await client.post("/api/v1/products/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient):
    # Create product first
    payload = {
        "name": "Test Phone",
        "description": "Smart phone",
        "price": 699.00,
        "stock": 15,
        "category": "Electronics"
    }
    create_res = await client.post("/api/v1/products/", json=payload)
    product_id = create_res.json()["id"]

    # Get product
    response = await client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id

@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    response = await client.get("/api/v1/products/99999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_products(client: AsyncClient):
    # Create multiple products
    for i in range(3):
        await client.post("/api/v1/products/", json={
            "name": f"Item {i}",
            "description": "Desc",
            "price": 100.0 + i,
            "stock": 5,
            "category": "Books" if i % 2 == 0 else "Gadgets"
        })

    response = await client.get("/api/v1/products/?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3

@pytest.mark.asyncio
async def test_update_product(client: AsyncClient):
    # Create initial product
    create_res = await client.post("/api/v1/products/", json={
        "name": "Old Name",
        "price": 50.0,
        "stock": 5,
        "category": "Clothing"
    })
    product_id = create_res.json()["id"]

    # Update product
    update_payload = {
        "name": "New Name",
        "price": 75.0
    }
    response = await client.put(f"/api/v1/products/{product_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["price"] == 75.0

@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient):
    # Create product
    create_res = await client.post("/api/v1/products/", json={
        "name": "To Delete",
        "price": 10.0,
        "stock": 1,
        "category": "Misc"
    })
    product_id = create_res.json()["id"]

    # Delete product
    del_res = await client.delete(f"/api/v1/products/{product_id}")
    assert del_res.status_code == 204

    # Verify deleted
    get_res = await client.get(f"/api/v1/products/{product_id}")
    assert get_res.status_code == 404
