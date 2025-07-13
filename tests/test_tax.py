import pytest
from httpx import AsyncClient
import pytest_asyncio


@pytest_asyncio.fixture
def sample_tax_reduction():
    return {"province_id": 1, "tax_discount_percent": 15.0}


@pytest_asyncio.fixture
async def setup_province(session):
    from ttt.models.model_location import Province

    province = Province(name="Province For Tax", code="PFT")
    session.add(province)
    await session.commit()
    await session.refresh(province)
    return province.id


@pytest.mark.asyncio
async def test_create_tax_reduction(client, sample_tax_reduction, setup_province):
    sample_tax_reduction["province_id"] = setup_province
    response = await client.post("/tax_reductions/", json=sample_tax_reduction)
    assert response.status_code == 200
    data = response.json()
    assert data["province_id"] == setup_province
    assert data["tax_discount_percent"] == 15.0


@pytest.mark.asyncio
async def test_get_all_tax_reductions(client, sample_tax_reduction, setup_province):
    sample_tax_reduction["province_id"] = setup_province
    await client.post("/tax_reductions/", json=sample_tax_reduction)
    response = await client.get("/tax_reductions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_tax_reduction_by_id(client, sample_tax_reduction, setup_province):
    sample_tax_reduction["province_id"] = setup_province
    create_resp = await client.post("/tax_reductions/", json=sample_tax_reduction)
    tax_id = create_resp.json()["id"]

    response = await client.get(f"/tax_reductions/{tax_id}")
    assert response.status_code == 200
    assert response.json()["id"] == tax_id


@pytest.mark.asyncio
async def test_update_tax_reduction(client, sample_tax_reduction, setup_province):
    sample_tax_reduction["province_id"] = setup_province
    create_resp = await client.post("/tax_reductions/", json=sample_tax_reduction)
    tax_id = create_resp.json()["id"]

    updated = {"tax_discount_percent": 20.0}
    response = await client.put(f"/tax_reductions/{tax_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["tax_discount_percent"] == 20.0


@pytest.mark.asyncio
async def test_delete_tax_reduction(client, sample_tax_reduction, setup_province):
    sample_tax_reduction["province_id"] = setup_province
    create_resp = await client.post("/tax_reductions/", json=sample_tax_reduction)
    tax_id = create_resp.json()["id"]

    response = await client.delete(f"/tax_reductions/{tax_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]

    # Verify deleted
    get_resp = await client.get(f"/tax_reductions/{tax_id}")
    assert get_resp.status_code == 404
