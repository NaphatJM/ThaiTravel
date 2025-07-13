import pytest
from httpx import AsyncClient, ASGITransport
from decimal import Decimal
import pytest_asyncio

from ttt.main import app
from ttt.models import get_session, model_activity
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# ------------------- Fixtures -------------------


@pytest_asyncio.fixture(scope="session")
def event_loop():
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def engine():
    load_dotenv(".env.test")
    db_url = os.getenv("SQLDB_URL")
    if not db_url:
        raise RuntimeError("SQLDB_URL is not set in .env.test")
    engine = create_async_engine(db_url, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(session):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
    app.dependency_overrides.clear()


# ------------------- Helper -------------------


@pytest_asyncio.fixture
async def setup_tax_and_activity(session):
    from ttt.models.model_location import Province, TaxReduction

    province = Province(name="Test Province", code="TST")
    session.add(province)
    await session.flush()

    tax = TaxReduction(province_id=province.id, tax_discount_percent=10.0)
    session.add(tax)
    await session.commit()
    return province.id


# ------------------- Tests -------------------


@pytest.mark.asyncio
async def test_create_activity(client, setup_tax_and_activity):
    province_id = setup_tax_and_activity
    activity = {
        "user_id": 1,
        "description": "Test trip",
        "province_id": province_id,
        "amount": 100.0,
        "tax_return": 0.0,  # will be ignored
    }
    response = await client.post("/activities/", json=activity)
    assert response.status_code == 200
    assert Decimal(response.json()["ภาษีที่สามารถลดหย่อนได้"]) == Decimal("10.0")


@pytest.mark.asyncio
async def test_get_all_activities(client, setup_tax_and_activity):
    await test_create_activity(client, setup_tax_and_activity)
    response = await client.get("/activities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_get_activity_by_id(client, setup_tax_and_activity):
    await test_create_activity(client, setup_tax_and_activity)
    response = await client.get("/activities/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.asyncio
async def test_update_activity(client, setup_tax_and_activity):
    await test_create_activity(client, setup_tax_and_activity)
    updated = {"description": "Updated trip"}
    response = await client.put("/activities/1", json=updated)
    assert response.status_code == 200
    assert response.json()["description"] == "Updated trip"


@pytest.mark.asyncio
async def test_delete_activity(client, setup_tax_and_activity):
    await test_create_activity(client, setup_tax_and_activity)
    response = await client.delete("/activities/1")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

    # verify deleted
    get_resp = await client.get("/activities/1")
    assert get_resp.status_code == 404
