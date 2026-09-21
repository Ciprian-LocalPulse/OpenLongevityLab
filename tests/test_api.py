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


def test_citation_export_excludes_synthetic_fixtures() -> None:
    client = TestClient(create_app())
    response = client.get("/api/v1/evidence/export/citation", params={"topic": "senescence"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "citation-eligible"
    assert payload["source_mode"] == "fixture-only"
    assert payload["items"] == []
    assert payload["total"] == 0
    assert payload["excluded_total"] == 1
    assert payload["excluded"][0]["identifier"] == "SYN-001"
    assert payload["excluded"][0]["reason"] == "synthetic_fixture"


def test_review_endpoint_is_disabled_without_review_key() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/evidence/SYN-001/review",
        json={
            "status": "verified",
            "reviewer": "Reviewer",
            "reviewed_at": "2026-09-21T10:00:00+03:00",
            "notes": "Checked against fixture source.",
        },
    )
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "REVIEW_DISABLED"


def test_review_endpoint_requires_database_for_persistence() -> None:
    client = TestClient(create_app(review_key="review-secret"))
    response = client.post(
        "/api/v1/evidence/SYN-001/review",
        headers={"X-Review-Key": "review-secret"},
        json={
            "status": "verified",
            "reviewer": "Reviewer",
            "reviewed_at": "2026-09-21T10:00:00+03:00",
            "notes": "Checked against fixture source.",
        },
    )
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "DATABASE_NOT_CONFIGURED"


def test_review_endpoint_rejects_machine_status_as_human_review() -> None:
    client = TestClient(create_app(review_key="review-secret"))
    response = client.post(
        "/api/v1/evidence/SYN-001/review",
        headers={"X-Review-Key": "review-secret"},
        json={
            "status": "machine_extracted",
            "reviewer": "Reviewer",
            "reviewed_at": "2026-09-21T10:00:00+03:00",
            "notes": "Machine extraction is not verification.",
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_REVIEW"
