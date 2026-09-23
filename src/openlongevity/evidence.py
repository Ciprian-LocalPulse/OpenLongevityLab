"""Transparent evidence grading rules."""

from collections import Counter, defaultdict
from collections.abc import Iterable
from datetime import UTC, datetime
from enum import StrEnum

from .models import (
    Contradiction,
    EvidenceRecord,
    FindingDirection,
    RetractionStatus,
    StudyType,
)


class EvidenceLevel(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"


_LEVEL_BY_TYPE = {
    StudyType.SYSTEMATIC_REVIEW: EvidenceLevel.A,
    StudyType.RCT: EvidenceLevel.B,
    StudyType.CLINICAL: EvidenceLevel.C,
    StudyType.OBSERVATIONAL: EvidenceLevel.D,
    StudyType.ANIMAL: EvidenceLevel.E,
    StudyType.IN_VITRO: EvidenceLevel.F,
    StudyType.COMPUTATIONAL: EvidenceLevel.G,
}

_BASE_SCORE = {
    StudyType.SYSTEMATIC_REVIEW: 0.95,
    StudyType.RCT: 0.85,
    StudyType.CLINICAL: 0.70,
    StudyType.OBSERVATIONAL: 0.50,
    StudyType.ANIMAL: 0.35,
    StudyType.IN_VITRO: 0.20,
    StudyType.COMPUTATIONAL: 0.10,
}


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _parse_publication_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return _utc_datetime(parsed)


class EvidenceEngine:
    """Grade and summarize records without implying clinical effectiveness."""

    def grade(self, record: EvidenceRecord) -> EvidenceLevel:
        if record.retraction_status is RetractionStatus.RETRACTED:
            return EvidenceLevel.G
        return _LEVEL_BY_TYPE[record.study_type]

    def score_components(
        self, record: EvidenceRecord, *, as_of: datetime | None = None
    ) -> dict[str, float | str | None]:
        """Return auditable navigation-score components for one evidence record."""
        scoring_time = _utc_datetime(as_of) if as_of else datetime.now(UTC)
        base_score = _BASE_SCORE[record.study_type]
        replication_status = record.replication_status.casefold()
        replication_multiplier = 1.0
        if replication_status in {"replicated", "independent"}:
            replication_multiplier = 1.15
        elif replication_status in {"unreplicated", "unknown"}:
            replication_multiplier = 0.85

        sample_size_multiplier = 1.0
        if record.sample_size is not None:
            sample_size_multiplier = min(
                1.15, 0.85 + (record.sample_size / (record.sample_size + 200))
            )

        publication_age_years: float | None = None
        publication_age_multiplier = 1.0
        if record.publication_date:
            try:
                publication_age_years = max(
                    0.0,
                    (scoring_time - _parse_publication_datetime(record.publication_date)).days
                    / 365.25,
                )
                publication_age_multiplier = max(0.75, 1.0 - publication_age_years * 0.01)
            except ValueError:
                publication_age_years = None

        retraction_multiplier = (
            0.0 if record.retraction_status is RetractionStatus.RETRACTED else 1.0
        )
        raw_score = (
            base_score
            * record.confidence
            * replication_multiplier
            * sample_size_multiplier
            * publication_age_multiplier
            * retraction_multiplier
        )
        bounded_score = round(min(1.0, max(0.0, raw_score)), 4)
        return {
            "method": "navigation-score-v1",
            "base_score": base_score,
            "confidence": record.confidence,
            "replication_multiplier": replication_multiplier,
            "sample_size_multiplier": round(sample_size_multiplier, 6),
            "publication_age_years": round(publication_age_years, 6)
            if publication_age_years is not None
            else None,
            "publication_age_multiplier": round(publication_age_multiplier, 6),
            "retraction_multiplier": retraction_multiplier,
            "bounded_score": bounded_score,
        }

    def score(self, record: EvidenceRecord, *, as_of: datetime | None = None) -> float:
        """Return a transparent navigation score, not a validated effect estimate.

        ``as_of`` freezes the publication-age component for reproducible reports. When
        omitted, the current UTC time preserves the historical runtime behavior.
        """
        return float(self.score_components(record, as_of=as_of)["bounded_score"])

    def summarize(
        self, records: Iterable[EvidenceRecord], *, as_of: datetime | None = None
    ) -> dict[str, object]:
        records = tuple(records)
        active = tuple(r for r in records if r.retraction_status is not RetractionStatus.RETRACTED)
        scoring_time = _utc_datetime(as_of) if as_of else datetime.now(UTC)
        grades = Counter(self.grade(r).value for r in active)
        mean = sum(r.confidence for r in active) / len(active) if active else 0.0
        return {
            "records": len(records),
            "active_records": len(active),
            "evidence_distribution": dict(sorted(grades.items())),
            "mean_confidence": round(mean, 4),
            "mean_navigation_score": round(
                sum(self.score(r, as_of=scoring_time) for r in active) / len(active), 4
            )
            if active
            else 0.0,
            "scoring_as_of": scoring_time.isoformat(),
            "disclaimer": "Research use only. Not medical advice.",
        }

    def contradictions(self, records: Iterable[EvidenceRecord]) -> list[Contradiction]:
        """Report mixed directional findings without resolving them automatically."""
        groups: dict[str, list[EvidenceRecord]] = defaultdict(list)
        for record in records:
            groups[" ".join(record.tags).casefold()].append(record)
        results: list[Contradiction] = []
        for topic, grouped in groups.items():
            positive = tuple(
                r.identifier for r in grouped if r.direction is FindingDirection.POSITIVE
            )
            negative = tuple(
                r.identifier for r in grouped if r.direction is FindingDirection.NEGATIVE
            )
            if positive and negative:
                results.append(
                    Contradiction(
                        topic,
                        positive,
                        negative,
                        "Records report opposing directions; review endpoints and populations.",
                    )
                )
        return results
