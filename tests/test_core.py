from datetime import UTC, datetime

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


def test_navigation_score_accepts_explicit_scoring_time() -> None:
    engine = EvidenceEngine()
    dated = record(
        "dated",
        StudyType.RCT,
        publication_date="2020-01-01",
        replication_status="replicated",
        sample_size=200,
    )
    early = datetime(2021, 1, 1, tzinfo=UTC)
    later = datetime(2031, 1, 1, tzinfo=UTC)

    assert engine.score(dated, as_of=early) == engine.score(dated, as_of=early)
    assert engine.score(dated, as_of=early) > engine.score(dated, as_of=later)

    summary = engine.summarize([dated], as_of=early)
    assert summary["scoring_as_of"] == "2021-01-01T00:00:00+00:00"
    assert summary["mean_navigation_score"] == engine.score(dated, as_of=early)


def test_gap_detector_flags_translation_gap() -> None:
    gaps = ResearchGapDetector().detect("senescence", [record("a", StudyType.ANIMAL)])
    assert gaps[0].kind == "translational_gap"


def test_graph_lists_neighbors() -> None:
    graph = EvidenceGraph()
    graph.add_edge("TP53", "associated_with", "senescence")
    assert graph.neighbors("TP53")[0]["object"] == "senescence"
