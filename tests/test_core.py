from openlongevity.evidence import EvidenceEngine, EvidenceLevel
from openlongevity.gaps import ResearchGapDetector
from openlongevity.graph import EvidenceGraph
from openlongevity.models import EvidenceRecord, RetractionStatus, StudyType


def record(identifier: str, study_type: StudyType, **kwargs) -> EvidenceRecord:
    return EvidenceRecord(
        identifier,
        "senescence study",
        study_type,
        "mouse",
        "healthspan",
        "fixture",
        confidence=0.8,
        tags=("senescence",),
        **kwargs,
    )


def test_grading_and_retraction() -> None:
    assert EvidenceEngine().grade(record("a", StudyType.RCT)) is EvidenceLevel.B
    assert (
        EvidenceEngine().grade(
            record("b", StudyType.ANIMAL, retraction_status=RetractionStatus.RETRACTED)
        )
        is EvidenceLevel.G
    )


def test_gap_detector_flags_translation_gap() -> None:
    gaps = ResearchGapDetector().detect("senescence", [record("a", StudyType.ANIMAL)])
    assert gaps[0].kind == "translational_gap"


def test_graph_lists_neighbors() -> None:
    graph = EvidenceGraph()
    graph.add_edge("TP53", "associated_with", "senescence")
    assert graph.neighbors("TP53")[0]["object"] == "senescence"
