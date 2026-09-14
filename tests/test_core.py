from openlongevity.evidence import EvidenceEngine, EvidenceLevel
from openlongevity.gaps import ResearchGapDetector
from openlongevity.graph import EvidenceGraph
from openlongevity.models import EvidenceRecord, RetractionStatus, StudyType


def record(identifier: str, study_type: StudyType, title: str = "senescence study", **kwargs) -> EvidenceRecord:
    return EvidenceRecord(identifier, title, study_type, "mouse", "lifespan", "fixture", confidence=0.8, tags=("senescence",), **kwargs)


def test_grading_and_retraction() -> None:
    engine = EvidenceEngine()
    assert engine.grade(record("a", StudyType.RCT)) is EvidenceLevel.B
    assert engine.grade(record("b", StudyType.ANIMAL, retraction_status=RetractionStatus.RETRACTED)) is EvidenceLevel.G


def test_gap_detector_flags_translation_gap() -> None:
    gaps = ResearchGapDetector().detect("senescence", [record("a", StudyType.ANIMAL)])
    assert gaps and gaps[0].kind == "translational_gap"


def test_graph_rejects_empty_and_lists_neighbors() -> None:
    graph = EvidenceGraph()
    graph.add_edge("TP53", "associated_with", "senescence")
    assert graph.neighbors("TP53") == [{"relation": "associated_with", "object": "senescence"}]
