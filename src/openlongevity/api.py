"""Optional FastAPI application exposing research primitives."""
from . import __version__
from .evidence import EvidenceEngine
from .gaps import ResearchGapDetector
from .graph import EvidenceGraph
from .models import EvidenceRecord, StudyType

try:
    from fastapi import FastAPI, Query
except ImportError:  # pragma: no cover
    FastAPI = None  # type: ignore[assignment,misc]

def create_app():
    if FastAPI is None:
        raise RuntimeError("Install openlongevity[api] to run the HTTP service")
    app = FastAPI(title="OpenLongevity API", version=__version__)
    engine = EvidenceEngine()
    detector = ResearchGapDetector(engine)
    graph = EvidenceGraph()
    graph.add_edge("TP53", "associated_with", "cellular senescence")
    fixture = [
        EvidenceRecord(
            "SYN-001",
            "Cellular senescence pathway study",
            StudyType.IN_VITRO,
            "human cells",
            "senescence markers",
            "synthetic fixture",
            confidence=0.55,
            tags=("cellular senescence",),
        ),
        EvidenceRecord(
            "SYN-002",
            "Senescence intervention in mice",
            StudyType.ANIMAL,
            "mouse",
            "healthspan",
            "synthetic fixture",
            confidence=0.60,
            replication_status="unreplicated",
            tags=("cellular senescence",),
        ),
    ]
    @app.get("/api/v1/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}
    @app.get("/api/v1/version")
    def version() -> dict[str, str]: return {"version": __version__}
    @app.get("/api/v1/evidence")
    def evidence(topic: str | None = Query(default=None, max_length=120)) -> dict[str, object]:
        records = [
            r
            for r in fixture
            if topic is None
            or topic.casefold() in r.title.casefold()
            or any(topic.casefold() in t.casefold() for t in r.tags)
        ]
        return {
            "items": [
                {"id": r.identifier, "title": r.title, "level": engine.grade(r).value}
                for r in records
            ],
            "summary": engine.summarize(records),
        }
    @app.get("/api/v1/research-gaps")
    def research_gaps(topic: str = Query(min_length=1, max_length=120)) -> dict[str, object]:
        return {
            "topic": topic,
            "gaps": [gap.__dict__ for gap in detector.detect(topic, fixture)],
        }
    @app.get("/api/v1/graph")
    def knowledge_graph(
        subject: str | None = Query(default=None, max_length=120),
    ) -> dict[str, object]:
        nodes = graph.neighbors(subject) if subject else graph.as_dict()
        return {"nodes": nodes}
    @app.get("/api/v1/search")
    def search(query: str = Query(min_length=1, max_length=120)) -> dict[str, object]:
        q = query.casefold()
        identifiers = [
            r.identifier
            for r in fixture
            if q in r.title.casefold() or any(q in t.casefold() for t in r.tags)
        ]
        return {"query": query, "identifiers": identifiers}
    return app
