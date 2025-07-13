import pytest
from httpx import AsyncClient
import pytest_asyncio


@pytest_asyncio.fixture
def sample_user():
    return {
        "full_name": "Jane Doe",
        "citizen_id": "1234567890123",
        "email": "jane@example.com",
        "phone": "0800000000",
        "address": "123 Test Street",
        "is_admin": False,
        "password": "securepassword123",
    }


@pytest.mark.asyncio
async def test_create_user(client, sample_user):
    response = await client.post("/users/", json=sample_user)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == sample_user["full_name"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_users(client, sample_user):
    await client.post("/users/", json=sample_user)
    response = await client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_get_user_by_id(client, sample_user):
    create_resp = await client.post("/users/", json=sample_user)
    user_id = create_resp.json()["id"]

    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id


@pytest.mark.asyncio
async def test_update_user(client, sample_user):
    create_resp = await client.post("/users/", json=sample_user)
    user_id = create_resp.json()["id"]

    updated_data = {"full_name": "Jane Updated"}
    response = await client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Jane Updated"


@pytest.mark.asyncio
async def test_delete_user(client, sample_user):
    create_resp = await client.post("/users/", json=sample_user)
    user_id = create_resp.json()["id"]

    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # ตรวจสอบว่าไม่มีแล้ว
    get_resp = await client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404
