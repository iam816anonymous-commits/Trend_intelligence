import pytest
from httpx import AsyncClient, ASGITransport
from backend.api.main import app

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Trend Intelligence AI India"}

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    # We expect status to be unhealthy if DBs are not running in test env
    # but the endpoint itself should be reachable and return JSON.
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "redis" in data
    assert "qdrant" in data
