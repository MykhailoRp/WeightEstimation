from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from api.main import app


@pytest.mark.asyncio
async def test_api_heakcheck_normal(alembic_headed: None) -> None:

    api_client = TestClient(app=app)

    response = api_client.get("api/health")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_api_heakcheck_failed(alembic_headed: None, monkeypatch: pytest.MonkeyPatch) -> None:

    async def mock_scalar(*args: Any, **kwargs: Any) -> None:
        raise OperationalError("EXPECTED ERROR", params=None, orig=Exception("EXPECTED ERROR"))

    monkeypatch.setattr(AsyncSession, "scalar", mock_scalar)

    api_client = TestClient(app=app)

    response = api_client.get("api/health")

    assert response.status_code == 503
