"""Typed domain models used by the evidence engine and API."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class StudyType(str, Enum):
    SYSTEMATIC_REVIEW = "systematic_review"
    RCT = "randomized_controlled_trial"
    CLINICAL = "clinical"
    OBSERVATIONAL = "observational"
    ANIMAL = "animal"
    IN_VITRO = "in_vitro"
    COMPUTATIONAL = "computational"

class RetractionStatus(str, Enum):
    ACTIVE = "active"
    CORRECTED = "corrected"
    EXPRESSION_OF_CONCERN = "expression_of_concern"
    RETRACTED = "retracted"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class EvidenceRecord:
    identifier: str
    title: str
    study_type: StudyType
    species: str
    endpoint: str
    source: str
    publication_date: str | None = None
    sample_size: int | None = None
    confidence: float = 0.0
    limitations: tuple[str, ...] = ()
    replication_status: str = "unknown"
    retraction_status: RetractionStatus = RetractionStatus.UNKNOWN
    tags: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.identifier.strip() or not self.title.strip() or not self.source.strip():
            raise ValueError("identifier, title, and source must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.sample_size is not None and self.sample_size < 0:
            raise ValueError("sample_size cannot be negative")

@dataclass(frozen=True)
class ResearchGap:
    topic: str
    kind: str
    rationale: str
    priority: str
    supporting_record_ids: tuple[str, ...]
