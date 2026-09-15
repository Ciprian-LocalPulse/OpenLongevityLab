"""Publication persistence with an immutable revision history."""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from .db import Database, PublicationRevisionRow, PublicationRow
from .providers.base import Publication


class PublicationRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    async def save(self, publication: Publication) -> dict[str, Any]:
        provenance = publication.provenance
        if provenance is None or not provenance.checksum:
            raise ValueError("Persistent publications require provenance and a source checksum")
        payload = asdict(publication)
        stable = asdict(publication)
        stable["provenance"].pop("retrieved_at")
        digest = hashlib.sha256(
            json.dumps(stable, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()
        async with self.database.sessions.begin() as session:
            # PostgreSQL ON CONFLICT serializes concurrent first inserts by source identity.
            created = await session.scalar(
                insert(PublicationRow).values(
                    identifier=publication.identifier, provider=provenance.source_provider,
                    source_identifier=provenance.source_identifier, title=publication.title,
                    payload=payload, content_hash=digest, revision=1,
                    first_retrieved_at=provenance.retrieved_at,
                    last_retrieved_at=provenance.retrieved_at,
                ).on_conflict_do_nothing(index_elements=["identifier"]).returning(
                    PublicationRow.identifier
                )
            )
            row = await session.scalar(
                select(PublicationRow).where(
                    PublicationRow.identifier == publication.identifier
                ).with_for_update()
            )
            if row is None:
                raise RuntimeError("Publication insert did not produce a row")
            changed = bool(created) or row.content_hash != digest
            if not created and changed:
                row.revision += 1
                row.payload, row.content_hash, row.title = payload, digest, publication.title
            # Unchanged retrievals update freshness without rewriting historical observations.
            row.last_retrieved_at = max(row.last_retrieved_at, provenance.retrieved_at)
            if changed:
                session.add(PublicationRevisionRow(
                    publication_id=row.identifier, revision=row.revision, payload=payload,
                    content_hash=digest, retrieved_at=provenance.retrieved_at,
                ))
            return self.serialize(row)

    @staticmethod
    def serialize(row: PublicationRow) -> dict[str, Any]:
        return {**row.payload, "revision": row.revision, "synthetic": False,
                "first_retrieved_at": row.first_retrieved_at,
                "last_retrieved_at": row.last_retrieved_at}

    async def get(self, identifier: str) -> dict[str, Any] | None:
        async with self.database.sessions() as session:
            row = await session.get(PublicationRow, identifier)
            return self.serialize(row) if row else None

    async def list(self, query: str, page: int, page_size: int) -> tuple[list[dict[str, Any]], int]:
        async with self.database.sessions() as session:
            condition = PublicationRow.title.icontains(query, autoescape=True)
            total = await session.scalar(select(func.count()).select_from(PublicationRow).where(
                condition
            ))
            rows = await session.scalars(select(PublicationRow).where(condition).order_by(
                PublicationRow.identifier
            ).offset((page - 1) * page_size).limit(page_size))
            return [self.serialize(row) for row in rows], int(total or 0)

    async def history(self, identifier: str) -> list[dict[str, Any]]:
        async with self.database.sessions() as session:
            rows = await session.scalars(select(PublicationRevisionRow).where(
                PublicationRevisionRow.publication_id == identifier
            ).order_by(PublicationRevisionRow.revision))
            return [{"revision": row.revision, "payload": row.payload,
                     "content_hash": row.content_hash, "retrieved_at": row.retrieved_at}
                    for row in rows]

