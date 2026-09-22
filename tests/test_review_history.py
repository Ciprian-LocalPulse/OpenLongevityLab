"""PostgreSQL review audit round-trip and cursor isolation contracts."""

import os
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from openlongevity.api import create_app
from openlongevity.db import Database, EvidenceReviewEventRow
from openlongevity.repository import EvidenceReviewRepository

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
pytestmark = [
    pytest.mark.postgres,
    pytest.mark.skipif(not TEST_DATABASE_URL, reason="TEST_DATABASE_URL is required"),
]


async def test_review_history_round_trip_and_cursor() -> None:
    assert TEST_DATABASE_URL is not None
    database = Database(TEST_DATABASE_URL)
    repository = EvidenceReviewRepository(database)
    reviewer = f"test-{uuid4()}"
    app = create_app(database_url=TEST_DATABASE_URL, review_key="test-review-key")
    try:
        async with app.router.lifespan_context(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test",
            ) as client:
                body = {"status": "verified", "reviewer": reviewer,
                        "reviewed_at": "2026-09-22T10:00:00+03:00", "notes": "Fixture review."}
                unauthorized = await client.post("/api/v1/evidence/SYN-001/review", json=body)
                assert unauthorized.status_code == 401
                created = []
                for status in ("verified", "disputed", "human_reviewed"):
                    response = await client.post(
                        "/api/v1/evidence/SYN-001/review",
                        json={**body, "status": status,
                              "reviewed_at": f"2026-09-{22 - len(created)}T10:00:00+03:00"},
                        headers={"X-Review-Key": "test-review-key"},
                    )
                    assert response.status_code == 200
                    created.append(response.json()["item"])
                    detail = (await client.get("/api/v1/evidence/SYN-001")).json()["item"]
                    assert detail["review_status"] == status
                    assert detail["reviewed_by"] == reviewer
                    assert detail["synthetic"] is True
                # Another record must never leak into this record's cursor page.
                await repository.record_event(
                    record_identifier=f"OTHER-{reviewer}", status="verified", reviewer=reviewer,
                    reviewed_at=body["reviewed_at"], notes=body["notes"], payload={},
                )
                first = (await client.get(
                    "/api/v1/evidence/SYN-001/review-events",
                    params={"after_id": created[0]["id"] - 1, "limit": 2},
                )).json()
                assert first["items"] == created[:2]
                assert first["next_after_id"] == created[1]["id"]
                second = (await client.get(
                    "/api/v1/evidence/SYN-001/review-events",
                    params={"after_id": first["next_after_id"], "limit": 2},
                )).json()
                assert second["items"] == created[2:]
                assert second["next_after_id"] is None
                empty, cursor = await repository.list_for_record(
                    "SYN-001", after_id=created[-1]["id"], limit=2,
                )
                assert (empty, cursor) == ([], None)
                # Reviewing a fixture never makes it a citable observation.
                exported = (await client.get("/api/v1/evidence/export/citation")).json()
                assert exported["items"] == []
                assert exported["excluded"][0]["reason"] == "synthetic_fixture"
                latest = await repository.latest_for_records(["SYN-001", "MISSING"])
                assert latest == {"SYN-001": created[-1]}
                assert await repository.latest_for_records([]) == {}
        # A fresh application instance must recover the same persisted review.
        restarted = create_app(database_url=TEST_DATABASE_URL)
        async with restarted.router.lifespan_context(restarted):
            async with AsyncClient(
                transport=ASGITransport(app=restarted), base_url="http://test",
            ) as client:
                response = await client.get("/api/v1/evidence", params={"topic": "senescence"})
                assert response.status_code == 200
                current = response.json()["items"][0]
                assert current["review_status"] == "human_reviewed"
                assert current["reviewed_by"] == reviewer
                assert current["reviewed_at"] == created[-1]["reviewed_at"]
                assert current["review_notes"] == body["notes"]
    finally:
        async with database.sessions.begin() as session:
            await session.execute(delete(EvidenceReviewEventRow).where(
                EvidenceReviewEventRow.reviewer == reviewer,
            ))
        await database.close()
