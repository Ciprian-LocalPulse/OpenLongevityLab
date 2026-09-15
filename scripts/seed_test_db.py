"""Seed the CI/test database with one publication so the /search contract test
has a real, matching row to find. Safe to run more than once: uses
ON CONFLICT DO NOTHING on the same (provider, source_identifier) pair the
production save() path already relies on for idempotency.
"""
import asyncio
import os

from sqlalchemy.dialects.postgresql import insert as pg_insert

from openlongevity.db import Database, PublicationRow

SEED_IDENTIFIER = "SEED-0001"
SEED_PROVIDER = "pubmed"
SEED_SOURCE_IDENTIFIER = "seed-0001"
SEED_TITLE = "Cellular senescence pathway study"
RETRIEVED_AT = "2026-01-01T00:00:00Z"

SEED_PAYLOAD = {
    "identifier": SEED_IDENTIFIER,
    "title": SEED_TITLE,
    "abstract": "Synthetic seed record used only for CI contract tests.",
    "authors": [],
    "journal": None,
    "publication_date": None,
    "doi": None,
    "publication_types": [],
    "mesh_terms": [],
    "citation_count": None,
    "provenance": {
        "source_provider": SEED_PROVIDER,
        "source_identifier": SEED_SOURCE_IDENTIFIER,
        "source_url": "https://example.invalid/seed-0001",
        "retrieved_at": RETRIEVED_AT,
        "source_updated_at": None,
        "license": None,
        "checksum": "seed-checksum",
        "normalization_version": "test",
        "parser_version": "test",
    },
    "retraction_status": "unknown",
    "corrections": [],
}


async def main() -> None:
    database_url = os.getenv("TEST_DATABASE_URL") or os.environ["DATABASE_URL"]
    database = Database(database_url)
    stmt = (
        pg_insert(PublicationRow)
        .values(
            identifier=SEED_IDENTIFIER,
            provider=SEED_PROVIDER,
            source_identifier=SEED_SOURCE_IDENTIFIER,
            title=SEED_TITLE,
            payload=SEED_PAYLOAD,
            content_hash="seed-checksum",
            revision=1,
            first_retrieved_at=RETRIEVED_AT,
            last_retrieved_at=RETRIEVED_AT,
        )
        .on_conflict_do_nothing(index_elements=["provider", "source_identifier"])
    )
    async with database.sessions() as session:
        await session.execute(stmt)
        await session.commit()
    await database.close()
    print(f"Seeded (or already present): {SEED_IDENTIFIER}")


if __name__ == "__main__":
    asyncio.run(main())
