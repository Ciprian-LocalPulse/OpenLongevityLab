import os
from unittest.mock import AsyncMock

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from openlongevity.api import create_app  # noqa: E402
from openlongevity.repository import EvidenceReviewRepository  # noqa: E402

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


def test_evidence_without_database_retains_unreviewed_fixture(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with TestClient(create_app()) as client:
        detail = client.get("/api/v1/evidence/SYN-001").json()["item"]
        listed = client.get("/api/v1/evidence").json()["items"][0]
    assert detail == listed
    assert detail["review_status"] == "unreviewed"
    assert detail["synthetic"] is True


@pytest.mark.parametrize("path", [
    "/api/v1/evidence", "/api/v1/evidence/SYN-001", "/api/v1/evidence/export/citation",
])
def test_review_storage_failure_does_not_return_stale_evidence(
    monkeypatch: pytest.MonkeyPatch, path: str,
) -> None:
    from sqlalchemy.exc import SQLAlchemyError

    monkeypatch.setattr(
        EvidenceReviewRepository, "latest_for_records",
        AsyncMock(side_effect=SQLAlchemyError("storage unavailable")),
    )
    with TestClient(create_app(database_url="postgresql+asyncpg://localhost/unused")) as client:
        response = client.get(path)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "DATABASE_UNAVAILABLE"


@pytest.mark.parametrize("params", [
    {"limit": 0}, {"limit": 101}, {"after_id": -1}, {"after_id": "invalid"},
])
def test_review_history_rejects_invalid_pagination(params: dict[str, object]) -> None:
    with TestClient(create_app()) as client:
        response = client.get("/api/v1/evidence/SYN-001/review-events", params=params)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_REQUEST"


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


def test_evidence_summary_accepts_explicit_scoring_time() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/api/v1/evidence",
        params={"topic": "senescence", "scoring_as_of": "2021-01-01T00:00:00Z"},
    )

    assert response.status_code == 200
    assert response.json()["summary"]["scoring_as_of"] == "2021-01-01T00:00:00+00:00"


def test_evidence_summary_rejects_invalid_scoring_time() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/api/v1/evidence",
        params={"topic": "senescence", "scoring_as_of": "not-a-date"},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_SCORING_AS_OF"


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

def test_review_endpoint_requires_database_for_persistence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Ascundem variabilele de mediu doar pentru acest test,
    # astfel incat baza de date sa para neconfigurata
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("TEST_DATABASE_URL", raising=False)

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
