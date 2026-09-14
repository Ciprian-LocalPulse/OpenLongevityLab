"""Optional FastAPI application exposing research primitives."""

from dataclasses import asdict
from os import getenv

from . import __version__
from .evidence import EvidenceEngine
from .gaps import ResearchGapDetector
from .graph import EvidenceGraph
from .models import EvidenceRecord, StudyType
from .providers import ClinicalTrialsProvider, PubMedProvider, SearchQuery
from .providers.base import ProviderError

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

    catalogs: dict[str, list[dict[str, object]]] = {
        "genes": [{"id": "TP53", "symbol": "TP53", "description": "Synthetic graph fixture"}],
        "proteins": [],
        "pathways": [{"id": "senescence-pathway", "name": "Cellular senescence"}],
        "biomarkers": [{"id": "crp", "name": "C-reactive protein", "category": "inflammatory"}],
        "interventions": [],
        "publications": [],
        "trials": [],
        "hallmarks": [{"id": "cellular-senescence", "name": "Cellular senescence"}],
        "datasets": [],
    }

    def _collection(name: str, item_id: str | None = None) -> dict[str, object]:
        items = catalogs[name]
        if item_id is not None:
            items = [item for item in items if item.get("id") == item_id]
        return {"items": items, "total": len(items), "page": 1, "page_size": 100}

    @app.get("/api/v1/health")
    def health() -> dict[str, object]:
        return {
            "status": "ok",
            "version": __version__,
            "database": "not_configured",
            "providers": {"pubmed": "available", "clinicaltrials": "available"},
        }

    @app.get("/api/v1/health/database")
    async def database_health() -> dict[str, str]:
        url = getenv("DATABASE_URL")
        if not url:
            return {"status": "not_configured"}
        try:
            from .db import Database

            database = Database(url)
            status = await database.health()
            await database.close()
            return {"status": status}
        except (RuntimeError, ValueError):
            return {"status": "unavailable"}

    @app.get("/api/v1/version")
    def version() -> dict[str, str]:
        return {"version": __version__}

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
        payload = graph.neighbors(subject) if subject else graph.as_dict()
        return payload

    @app.get("/api/v1/search")
    def search(
        query: str = Query(min_length=1, max_length=120),
        limit: int = Query(default=25, ge=1, le=100),
    ) -> dict[str, object]:
        q = query.casefold()
        items = [
            {
                "id": r.identifier,
                "title": r.title,
                "type": "evidence",
                "level": engine.grade(r).value,
            }
            for r in fixture
            if q in r.title.casefold() or any(q in t.casefold() for t in r.tags)
        ][:limit]
        return {"query": query, "items": items, "total": len(items), "page": 1, "page_size": limit}

    for resource in catalogs:
        app.add_api_route(
            f"/api/v1/{resource}",
            lambda resource=resource: _collection(resource),
            methods=["GET"],
            name=f"list_{resource}",
        )
        app.add_api_route(
            f"/api/v1/{resource}/{{item_id}}",
            lambda item_id, resource=resource: _collection(resource, item_id),
            methods=["GET"],
            name=f"get_{resource}",
        )

    @app.get("/api/v1/evidence/{record_id}")
    def evidence_by_id(record_id: str) -> dict[str, object]:
        records = [record for record in fixture if record.identifier == record_id]
        if not records:
            return {"error": {"code": "NOT_FOUND", "message": "Evidence record was not found."}}
        record = records[0]
        return {
            "item": asdict(record),
            "level": engine.grade(record).value,
            "score": engine.score(record),
        }

    @app.post("/api/v1/ingestion/pubmed")
    async def ingest_pubmed(
        query: str = Query(min_length=1, max_length=120),
        limit: int = Query(default=10, ge=1, le=25),
    ) -> dict[str, object]:
        try:
            records = await PubMedProvider().search(SearchQuery(query, limit=limit))
        except ProviderError as exc:
            return {"error": {"code": "PROVIDER_UNAVAILABLE", "message": str(exc)}}
        return {
            "provider": "pubmed",
            "items": [asdict(record) for record in records],
            "count": len(records),
        }

    @app.post("/api/v1/ingestion/clinical-trials")
    async def ingest_trials(
        query: str = Query(min_length=1, max_length=120),
        limit: int = Query(default=10, ge=1, le=25),
    ) -> dict[str, object]:
        try:
            records = await ClinicalTrialsProvider().search(SearchQuery(query, limit=limit))
        except ProviderError as exc:
            return {"error": {"code": "PROVIDER_UNAVAILABLE", "message": str(exc)}}
        return {
            "provider": "clinicaltrials.gov",
            "items": [asdict(record) for record in records],
            "count": len(records),
        }

    return app
