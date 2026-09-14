"""Research-gap detection based on transparent, reviewable heuristics."""

from typing import Iterable

from .evidence import EvidenceEngine
from .models import EvidenceRecord, ResearchGap, StudyType


class ResearchGapDetector:
    def __init__(self, engine: EvidenceEngine | None = None) -> None:
        self.engine = engine or EvidenceEngine()

    def detect(self, topic: str, records: Iterable[EvidenceRecord]) -> list[ResearchGap]:
        """Identify evidence distribution gaps for a topic."""
        selected = tuple(r for r in records if topic.lower() in self._search_text(r))
        if not selected:
            return [ResearchGap(topic, "no_indexed_evidence", "No matching records were indexed.", "high", ())]
        ids = tuple(r.identifier for r in selected)
        types = {r.study_type for r in selected}
        gaps: list[ResearchGap] = []
        if StudyType.ANIMAL in types and not ({StudyType.CLINICAL, StudyType.RCT} & types):
            gaps.append(ResearchGap(topic, "translational_gap", "Animal evidence is present without indexed human clinical evidence.", "high", ids))
        if len({r.replication_status for r in selected}) == 1 and selected[0].replication_status in {"unknown", "unreplicated"}:
            gaps.append(ResearchGap(topic, "replication_gap", "Replication status is unknown or unreplicated across matching records.", "medium", ids))
        if len({r.source for r in selected}) == 1 and len(selected) > 1:
            gaps.append(ResearchGap(topic, "concentration", "Evidence is concentrated in one source, limiting independent corroboration.", "medium", ids))
        return gaps

    @staticmethod
    def _search_text(record: EvidenceRecord) -> str:
        return " ".join((record.title, record.endpoint, record.source, *record.tags)).lower()
