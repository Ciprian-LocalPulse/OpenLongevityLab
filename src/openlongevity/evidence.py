"""Transparent evidence grading rules."""
from collections import Counter
from enum import Enum
from typing import Iterable
from .models import EvidenceRecord, RetractionStatus, StudyType

class EvidenceLevel(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"

_LEVEL_BY_TYPE = {
    StudyType.SYSTEMATIC_REVIEW: EvidenceLevel.A, StudyType.RCT: EvidenceLevel.B,
    StudyType.CLINICAL: EvidenceLevel.C, StudyType.OBSERVATIONAL: EvidenceLevel.D,
    StudyType.ANIMAL: EvidenceLevel.E, StudyType.IN_VITRO: EvidenceLevel.F,
    StudyType.COMPUTATIONAL: EvidenceLevel.G,
}

class EvidenceEngine:
    """Grade and summarize records without implying clinical effectiveness."""
    def grade(self, record: EvidenceRecord) -> EvidenceLevel:
        if record.retraction_status is RetractionStatus.RETRACTED:
            return EvidenceLevel.G
        return _LEVEL_BY_TYPE[record.study_type]

    def summarize(self, records: Iterable[EvidenceRecord]) -> dict[str, object]:
        records = tuple(records)
        active = tuple(r for r in records if r.retraction_status is not RetractionStatus.RETRACTED)
        grades = Counter(self.grade(r).value for r in active)
        mean = sum(r.confidence for r in active) / len(active) if active else 0.0
        return {
            "records": len(records),
            "active_records": len(active),
            "evidence_distribution": dict(sorted(grades.items())),
            "mean_confidence": round(mean, 4),
            "disclaimer": "Research use only. Not medical advice.",
        }
