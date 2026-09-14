"""Data-access operations kept separate from HTTP and scientific logic."""

from .db import Database, EvidenceRow
from .models import EvidenceRecord


class EvidenceRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    async def save(self, record: EvidenceRecord, level: str) -> None:
        """Upsert one evidence record in a transaction."""
        if EvidenceRow is None:
            raise RuntimeError("Database support is not installed")
        async with self.database.sessions() as session:
            existing = await session.get(EvidenceRow, record.identifier)
            values = {
                "identifier": record.identifier,
                "study_type": record.study_type.value,
                "evidence_level": level,
                "species": record.species,
                "endpoint": record.endpoint,
                "confidence": record.confidence,
                "sample_size": record.sample_size,
                "provenance": record.metadata,
            }
            if existing is None:
                session.add(EvidenceRow(**values))
            else:
                for key, value in values.items():
                    setattr(existing, key, value)
            await session.commit()
