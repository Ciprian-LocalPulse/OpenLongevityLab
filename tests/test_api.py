import os

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from openlongevity.api import create_app  # noqa: E402

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


def test_health_contract() -> None:
    client = TestClient(create_app())
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["version"] == "0.3.0"


@pytest.mark.postgres
@pytest.mark.skipif(
    not TEST_DATABASE_URL,
    reason="TEST_DATABASE_URL is required for the PostgreSQL-backed search contract test",
)
def test_search_contract() -> None:
    client = TestClient(create_app(database_url=TEST_DATABASE_URL))
    search = client.get("/api/v1/search", params={"query": "senescence"})
    assert search.status_code == 200
    assert search.json()["total"] >= 1


def test_missing_evidence_is_structured() -> None:
    client = TestClient(create_app())
    payload = client.get("/api/v1/evidence/unknown").json()
    assert payload["error"]["code"] == "NOT_FOUND"
