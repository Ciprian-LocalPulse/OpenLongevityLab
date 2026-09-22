"""Publication persistence with an immutable revision history."""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from .db import Database, EvidenceReviewEventRow, PublicationRevisionRow, PublicationRow
from .origins import publication_origin_fields
from .providers.base import Publication


class PublicationRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    async def save(self, publication: Publication) -> dict[str, Any]:
        provenance = publication.provenance
        if provenance is None or not provenance.checksum:
            raise ValueError("Persistent publications require provenance and a source checksum")
        publication_payload = asdict(publication)
        payload = {**publication_payload, **publication_origin_fields(publication_payload)}
        stable = {**payload, "provenance": dict(payload["provenance"])}
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
        return {
            **row.payload,
            **publication_origin_fields(row.payload),
            "revision": row.revision,
            "first_retrieved_at": row.first_retrieved_at,
            "last_retrieved_at": row.last_retrieved_at,
        }

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
            return [
                {
                    "revision": row.revision,
                    "payload": {**row.payload, **publication_origin_fields(row.payload)},
                    "content_hash": row.content_hash,
                    "retrieved_at": row.retrieved_at,
                }
                for row in rows
            ]


class EvidenceReviewRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    async def latest_for_records(self, identifiers: list[str]) -> dict[str, dict[str, Any]]:
        """Read the greatest persisted event ID per record in one query."""
        if not identifiers:
            return {}
        latest_ids = select(func.max(EvidenceReviewEventRow.id)).where(
            EvidenceReviewEventRow.record_identifier.in_(identifiers),
        ).group_by(EvidenceReviewEventRow.record_identifier)
        async with self.database.sessions() as session:
            rows = await session.scalars(select(EvidenceReviewEventRow).where(
                EvidenceReviewEventRow.id.in_(latest_ids),
            ))
            return {row.record_identifier: self.serialize(row) for row in rows}

    async def record_event(
        self,
        *,
        record_identifier: str,
        status: str,
        reviewer: str,
        reviewed_at: str,
        notes: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        async with self.database.sessions.begin() as session:
            row = EvidenceReviewEventRow(
                record_identifier=record_identifier,
                status=status,
                reviewer=reviewer,
                reviewed_at=reviewed_at,
                notes=notes,
                payload=payload,
            )
            session.add(row)
            await session.flush()
            return self.serialize(row)

    async def list_for_record(
        self, record_identifier: str, *, after_id: int = 0, limit: int = 50,
    ) -> tuple[list[dict[str, Any]], int | None]:
        if after_id < 0 or not 1 <= limit <= 100:
            raise ValueError("Review history requires after_id >= 0 and limit between 1 and 100")
        async with self.database.sessions() as session:
            rows = await session.scalars(select(EvidenceReviewEventRow).where(
                EvidenceReviewEventRow.record_identifier == record_identifier,
                EvidenceReviewEventRow.id > after_id,
            ).order_by(EvidenceReviewEventRow.id).limit(limit + 1))
            items = [self.serialize(row) for row in rows]
            next_after_id = items[limit - 1]["id"] if len(items) > limit else None
            return items[:limit], next_after_id

    @staticmethod
    def serialize(row: EvidenceReviewEventRow) -> dict[str, Any]:
        return {
            "id": row.id,
            "record_identifier": row.record_identifier,
            "status": row.status,
            "reviewer": row.reviewer,
            "reviewed_at": row.reviewed_at,
            "notes": row.notes,
            "payload": row.payload,
        }

