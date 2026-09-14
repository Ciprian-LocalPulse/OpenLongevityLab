"""Research-gap detection based on transparent heuristics."""

from collections.abc import Iterable

from .evidence import EvidenceEngine
from .models import EvidenceRecord, ResearchGap, StudyType


class ResearchGapDetector:
    def __init__(self, engine: EvidenceEngine | None = None) -> None:
        self.engine = engine or EvidenceEngine()

    def detect(self, topic: str, records: Iterable[EvidenceRecord]) -> list[ResearchGap]:
        selected = tuple(r for r in records if topic.casefold() in self._search_text(r))
        if not selected:
            return [
                ResearchGap(
                    topic,
                    "no_indexed_evidence",
                    "No matching records were indexed.",
                    "high",
                    (),
                )
            ]
        ids = tuple(r.identifier for r in selected)
        types = {r.study_type for r in selected}
        gaps: list[ResearchGap] = []
        if StudyType.ANIMAL in types and not ({StudyType.CLINICAL, StudyType.RCT} & types):
            gaps.append(
                ResearchGap(
                    topic,
                    "translational_gap",
                    "Animal evidence is present without indexed human clinical evidence.",
                    "high",
                    ids,
                    0.81,
                )
            )
        if StudyType.IN_VITRO in types and StudyType.ANIMAL not in types:
            gaps.append(
                ResearchGap(
                    topic,
                    "validation_gap",
                    "In-vitro evidence is present without indexed animal validation.",
                    "high",
                    ids,
                    0.78,
                )
            )
        if all(r.replication_status in {"unknown", "unreplicated"} for r in selected):
            gaps.append(
                ResearchGap(
                    topic,
                    "replication_gap",
                    "Replication status is unknown or unreplicated across matching records.",
                    "medium",
                    ids,
                    0.72,
                )
            )
        if len({r.source for r in selected}) == 1 and len(selected) > 1:
            gaps.append(
                ResearchGap(
                    topic,
                    "concentration",
                    "Evidence is concentrated in one source, limiting corroboration.",
                    "medium",
                    ids,
                    0.68,
                )
            )
        small = tuple(
            r.identifier for r in selected if r.sample_size is not None and r.sample_size < 50
        )
        if small:
            gaps.append(
                ResearchGap(
                    topic,
                    "small_sample",
                    "At least one matching record reports a small sample (<50).",
                    "medium",
                    small,
                    0.70,
                )
            )
        outdated = tuple(r.identifier for r in selected if r.metadata.get("outdated") is True)
        if outdated:
            gaps.append(
                ResearchGap(
                    topic,
                    "outdated_evidence",
                    "Matching records were marked outdated by the source refresh policy.",
                    "low",
                    outdated,
                    0.65,
                )
            )
        return gaps

    @staticmethod
    def _search_text(record: EvidenceRecord) -> str:
        return " ".join((record.title, record.endpoint, record.source, *record.tags)).casefold()
