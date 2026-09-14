"""Optional FastAPI application exposing the research primitives."""

from . import __version__
from .evidence import EvidenceEngine
from .models import EvidenceRecord, StudyType

try:
    from fastapi import FastAPI, Query
except ImportError:  # pragma: no cover - keeps the core package dependency-light
    FastAPI = None  # type: ignore[assignment,misc]


def create_app():
    if FastAPI is None:
        raise RuntimeError("Install openlongevity[api] to run the HTTP service")
    app = FastAPI(title="OpenLongevity API", version=__version__)
    engine = EvidenceEngine()
    fixture = [EvidenceRecord("SYN-001", "Cellular senescence pathway study", StudyType.IN_VITRO, "human cells", "senescence markers", "synthetic fixture", confidence=0.55, tags=("cellular senescence",))]

    @app.get("/api/v1/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    @app.get("/api/v1/evidence")
    def evidence(topic: str | None = Query(default=None, max_length=120)) -> dict[str, object]:
        records = [r for r in fixture if topic is None or topic.lower() in r.title.lower() or topic.lower() in r.tags]
        return {"items": [{"id": r.identifier, "title": r.title, "level": engine.grade(r).value} for r in records], "summary": engine.summarize(records)}

    return app
