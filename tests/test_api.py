import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from openlongevity.api import create_app  # noqa: E402


def test_health_and_search_contract() -> None:
    client = TestClient(create_app())
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["version"] == "0.2.0"
    search = client.get("/api/v1/search", params={"query": "senescence"})
    assert search.status_code == 200
    assert search.json()["total"] >= 1


def test_missing_evidence_is_structured() -> None:
    client = TestClient(create_app())
    payload = client.get("/api/v1/evidence/unknown").json()
    assert payload["error"]["code"] == "NOT_FOUND"
