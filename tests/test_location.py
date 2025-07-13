import pytest
from httpx import AsyncClient
import pytest_asyncio


@pytest_asyncio.fixture
def sample_province():
    return {"name": "Test Province", "code": "TPV"}


@pytest.mark.asyncio
async def test_create_province(client, sample_province):
    response = await client.post("/locations/provinces", json=sample_province)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_province["name"]
    assert data["code"] == sample_province["code"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_provinces(client, sample_province):
    await client.post("/locations/provinces", json=sample_province)
    response = await client.get("/locations/provinces")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(p["name"] == sample_province["name"] for p in data)


@pytest.mark.asyncio
async def test_get_province_by_id(client, sample_province):
    create_resp = await client.post("/locations/provinces", json=sample_province)
    province_id = create_resp.json()["id"]

    response = await client.get(f"/locations/provinces/{province_id}")
    assert response.status_code == 200
    assert response.json()["id"] == province_id


@pytest.mark.asyncio
async def test_update_province(client, sample_province):
    create_resp = await client.post("/locations/provinces", json=sample_province)
    province_id = create_resp.json()["id"]

    updated_data = {"name": "Updated Province Name"}
    response = await client.put(
        f"/locations/provinces/{province_id}", json=updated_data
    )
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]


@pytest.mark.asyncio
async def test_delete_province(client, sample_province):
    create_resp = await client.post("/locations/provinces", json=sample_province)
    province_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/locations/provinces/{province_id}")
    assert delete_resp.status_code == 200
    assert "deleted successfully" in delete_resp.json()["message"]

    get_resp = await client.get(f"/locations/provinces/{province_id}")
    assert get_resp.status_code == 404
