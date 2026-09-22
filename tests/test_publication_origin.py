"""Publication origin classification survives persistence, search, and history."""

import os
from dataclasses import replace
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from openlongevity.api import create_app
from openlongevity.db import Database, PublicationRevisionRow, PublicationRow
from openlongevity.origins import PublicationOrigin
from openlongevity.providers.base import Provenance, Publication
from openlongevity.repository import PublicationRepository

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
pytestmark = [
    pytest.mark.postgres,
    pytest.mark.skipif(not TEST_DATABASE_URL, reason="TEST_DATABASE_URL is required"),
]


async def test_publication_origin_survives_api_and_history_round_trip() -> None:
    assert TEST_DATABASE_URL is not None
    token = uuid4().hex
    database = Database(TEST_DATABASE_URL)
    repository = PublicationRepository(database)
    identifiers = [f"TEST-ORIGIN-{token}"]
    app = create_app(database_url=TEST_DATABASE_URL)
    try:
        initial = publication(
            identifier=identifiers[0],
            source_identifier=f"test-origin-{token}",
            title="Origin audit study",
            origin=PublicationOrigin.UNKNOWN,
        )
        saved = await repository.save(initial)
        assert saved["origin"] == "unknown"
        assert saved["synthetic"] is None
        assert saved["revision"] == 1

        # A clearer documented manual origin is a content-contract change.
        updated = await repository.save(replace(initial, origin=PublicationOrigin.MANUAL))
        assert updated["origin"] == "manual"
        assert updated["synthetic"] is None
        assert updated["revision"] == 2

        async with app.router.lifespan_context(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test",
            ) as client:
                detail = (await client.get(f"/api/v1/publications/{identifiers[0]}")).json()
                assert detail["origin"] == "manual"
                assert detail["synthetic"] is None

                search = (await client.get(
                    "/api/v1/search", params={"query": "Origin audit"},
                )).json()
                assert search["items"][0]["origin"] == "manual"
                assert search["items"][0]["synthetic"] is None

                history = (await client.get(
                    f"/api/v1/publications/{identifiers[0]}/history"
                )).json()
                assert [item["revision"] for item in history] == [1, 2]
                assert history[0]["payload"]["origin"] == "unknown"
                assert history[0]["payload"]["synthetic"] is None
                assert history[1]["payload"]["origin"] == "manual"
                assert history[1]["payload"]["synthetic"] is None
                assert history[0]["content_hash"] != history[1]["content_hash"]
    finally:
        await cleanup(database, identifiers)


async def test_synthetic_prefix_overrides_provider_shaped_metadata() -> None:
    assert TEST_DATABASE_URL is not None
    token = uuid4().hex
    identifier = f"SEED-{token}"
    database = Database(TEST_DATABASE_URL)
    repository = PublicationRepository(database)
    try:
        saved = await repository.save(publication(
            identifier=identifier,
            source_identifier=f"provider-shaped-{token}",
            title="Provider-shaped synthetic seed",
            origin=PublicationOrigin.PROVIDER,
        ))
        assert saved["origin"] == "synthetic"
        assert saved["synthetic"] is True
    finally:
        await cleanup(database, [identifier])


@pytest.mark.skipif(
    not TEST_DATABASE_URL,
    reason="TEST_DATABASE_URL is required for the PostgreSQL-backed search contract test",
)
def test_seed_publication_is_labeled_synthetic_in_search() -> None:
    app = create_app(database_url=TEST_DATABASE_URL)
    with TestClient(app) as client:
        response = client.get("/api/v1/search", params={"query": "senescence"})
    assert response.status_code == 200
    seed = next(
        item for item in response.json()["items"] if item["identifier"] == "SEED-0001"
    )
    assert seed["origin"] == "synthetic"
    assert seed["synthetic"] is True


def publication(
    *,
    identifier: str,
    source_identifier: str,
    title: str,
    origin: PublicationOrigin,
) -> Publication:
    return Publication(
        identifier=identifier,
        title=title,
        abstract="Synthetic integration fixture for persistence behavior.",
        provenance=Provenance(
            source_provider="test",
            source_identifier=source_identifier,
            source_url=f"https://example.invalid/{source_identifier}",
            retrieved_at="2026-09-22T00:00:00+00:00",
            checksum=f"checksum-{source_identifier}",
            normalization_version="test",
            parser_version="test",
        ),
        origin=origin,
    )


async def cleanup(database: Database, identifiers: list[str]) -> None:
    async with database.sessions.begin() as session:
        await session.execute(delete(PublicationRevisionRow).where(
            PublicationRevisionRow.publication_id.in_(identifiers)
        ))
        await session.execute(delete(PublicationRow).where(
            PublicationRow.identifier.in_(identifiers)
        ))
    await database.close()
