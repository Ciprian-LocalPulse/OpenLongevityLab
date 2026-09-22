"""Versioned publication API. Demo science is explicitly separated from persisted metadata."""
import secrets
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import asdict
from os import getenv
from typing import Any, Literal

from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import __version__
from .constants import DISCLAIMER
from .db import Database
from .evidence import EvidenceEngine
from .exports import build_citation_export, evidence_record_payload
from .gaps import ResearchGapDetector
from .models import EvidenceRecord, ReviewStatus, StudyType
from .origins import PublicationOrigin
from .providers import PubMedProvider, SearchQuery
from .providers.base import ProviderError
from .review import apply_human_review


class ProvenanceResponse(BaseModel):
    source_provider: str
    source_identifier: str
    source_url: str
    retrieved_at: str
    source_updated_at: str | None = None
    license: str | None = None
    checksum: str
    normalization_version: str
    parser_version: str


class PublicationResponse(BaseModel):
    identifier: str
    title: str
    abstract: str = ""
    authors: list[str] = Field(default_factory=list)
    journal: str | None = None
    publication_date: str | None = None
    doi: str | None = None
    publication_types: list[str] = Field(default_factory=list)
    mesh_terms: list[str] = Field(default_factory=list)
    citation_count: int | None = None
    provenance: ProvenanceResponse
    retraction_status: str = "unknown"
    corrections: list[dict[str, str]] = Field(default_factory=list)
    revision: int
    origin: PublicationOrigin
    synthetic: bool | None
    first_retrieved_at: str
    last_retrieved_at: str


class PublicationRevisionPayload(BaseModel):
    identifier: str
    title: str
    abstract: str = ""
    authors: list[str] = Field(default_factory=list)
    journal: str | None = None
    publication_date: str | None = None
    doi: str | None = None
    publication_types: list[str] = Field(default_factory=list)
    mesh_terms: list[str] = Field(default_factory=list)
    citation_count: int | None = None
    provenance: ProvenanceResponse
    retraction_status: str = "unknown"
    corrections: list[dict[str, str]] = Field(default_factory=list)
    origin: PublicationOrigin
    synthetic: bool | None


class PublicationPage(BaseModel):
    items: list[PublicationResponse]
    total: int
    page: int
    page_size: int
    mode: Literal["persisted"] = "persisted"
    disclaimer: str = DISCLAIMER


class IngestionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(min_length=1, max_length=200)
    limit: int = Field(default=5, ge=1, le=25)


class EvidenceReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: ReviewStatus
    reviewer: str = Field(min_length=1, max_length=120)
    reviewed_at: str = Field(min_length=1, max_length=40)
    notes: str = Field(min_length=1, max_length=2000)


class RevisionResponse(BaseModel):
    revision: int
    payload: PublicationRevisionPayload
    content_hash: str
    retrieved_at: str


def create_app(
    database_url: str | None = None, provider: PubMedProvider | None = None,
    ingestion_key: str | None = None, review_key: str | None = None,
) -> FastAPI:
    from .repository import EvidenceReviewRepository, PublicationRepository

    database_url = database_url or getenv("DATABASE_URL")
    database = Database(database_url) if database_url else None
    repository = PublicationRepository(database) if database else None
    review_repository = EvidenceReviewRepository(database) if database else None
    source = provider or PubMedProvider()
    key = ingestion_key if ingestion_key is not None else getenv("OPENLONGEVITY_INGESTION_KEY")
    reviewer_key = (
        review_key if review_key is not None else getenv("OPENLONGEVITY_REVIEW_KEY")
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        yield
        if database:
            await database.close()

    app = FastAPI(title="OpenLongevity API", version=__version__, lifespan=lifespan,
                  description=DISCLAIMER)
    origins = [o.strip() for o in getenv("OPENLONGEVITY_WEB_ORIGINS", "").split(",") if o.strip()]
    if origins:
        app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET"],
                           allow_headers=["Accept"], allow_credentials=False)

    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        detail = exc.detail if isinstance(exc.detail, dict) else {
            "code": "HTTP_ERROR", "message": str(exc.detail)
        }
        return JSONResponse({"error": detail}, status_code=exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse({"error": {"code": "INVALID_REQUEST",
                                      "message": "Request does not satisfy the API schema"}},
                            status_code=422)

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        return JSONResponse({"error": {"code": "DATABASE_UNAVAILABLE",
                                      "message": "Publication storage is unavailable"}},
                            status_code=503)

    def require_repository() -> PublicationRepository:
        if repository is None:
            raise HTTPException(503, {"code": "DATABASE_NOT_CONFIGURED",
                                      "message": "Configure and migrate PostgreSQL first"})
        return repository

    def require_review_repository() -> EvidenceReviewRepository:
        if review_repository is None:
            raise HTTPException(503, {"code": "DATABASE_NOT_CONFIGURED",
                                      "message": "Configure and migrate PostgreSQL first"})
        return review_repository

    @app.get("/api/v1/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__,
                "database": await database.health() if database else "not_configured",
                "provider_status": "not_probed", "disclaimer": DISCLAIMER}

    @app.get("/api/v1/version")
    def version() -> dict[str, str]:
        return {"version": __version__}

    @app.get("/api/v1/health/database")
    async def database_health() -> dict[str, str]:
        return {"status": await database.health() if database else "not_configured"}

    @app.post("/api/v1/ingestion/pubmed", response_model=PublicationPage)
    async def ingest_pubmed(
        body: IngestionRequest, x_ingestion_key: str | None = Header(default=None)
    ) -> PublicationPage:
        if not key:
            raise HTTPException(503, {"code": "INGESTION_DISABLED",
                                      "message": "Server-side ingestion key is not configured"})
        if not x_ingestion_key or not secrets.compare_digest(x_ingestion_key, key):
            raise HTTPException(401, {"code": "UNAUTHORIZED",
                                      "message": "An operator ingestion key is required"})
        repo = require_repository()
        try:
            records = await source.search(SearchQuery(body.query, limit=body.limit))
        except ValueError as exc:
            raise HTTPException(422, {"code": "INVALID_QUERY", "message": str(exc)}) from exc
        except ProviderError as exc:
            raise HTTPException(502, {"code": "PROVIDER_UNAVAILABLE",
                                      "message": "PubMed is unavailable; retry later"}) from exc
        items = [PublicationResponse.model_validate(await repo.save(record)) for record in records]
        return PublicationPage(items=items, total=len(items), page=1, page_size=body.limit)

    @app.get("/api/v1/publications", response_model=PublicationPage)
    @app.get("/api/v1/search", response_model=PublicationPage)
    async def publications(
        query: str = Query(default="", max_length=200),
        page: int = Query(default=1, ge=1, le=10000),
        page_size: int = Query(default=20, ge=1, le=100),
    ) -> PublicationPage:
        items, total = await require_repository().list(query.strip(), page, page_size)
        return PublicationPage(items=[PublicationResponse.model_validate(item) for item in items],
                               total=total, page=page, page_size=page_size)

    @app.get("/api/v1/publications/{identifier}", response_model=PublicationResponse)
    async def publication(identifier: str) -> PublicationResponse:
        if len(identifier) > 160:
            raise HTTPException(
                422, {"code": "INVALID_IDENTIFIER", "message": "Identifier too long"}
            )
        item = await require_repository().get(identifier)
        if item is None:
            raise HTTPException(404, {"code": "NOT_FOUND", "message": "Publication not found"})
        return PublicationResponse.model_validate(item)

    @app.get("/api/v1/publications/{identifier}/history", response_model=list[RevisionResponse])
    async def history(identifier: str) -> list[RevisionResponse]:
        await publication(identifier)
        return [
            RevisionResponse.model_validate(row)
            for row in await require_repository().history(identifier)
        ]

    engine = EvidenceEngine()
    fixtures = [EvidenceRecord(
        "SYN-001", "Synthetic senescence example", StudyType.IN_VITRO, "synthetic cells",
        "illustrative marker", "synthetic fixture", confidence=0.55, tags=("senescence",)
    )]

    async def current_records(records: list[EvidenceRecord]) -> list[EvidenceRecord]:
        if review_repository is None:
            return records
        events = await review_repository.latest_for_records([r.identifier for r in records])
        return [apply_human_review(
            record, status=ReviewStatus(events[record.identifier]["status"]),
            reviewer=events[record.identifier]["reviewer"],
            reviewed_at=events[record.identifier]["reviewed_at"],
            notes=events[record.identifier]["notes"],
        ) if record.identifier in events else record for record in records]

    @app.get("/api/v1/evidence")
    async def evidence(topic: str = Query(default="", max_length=120)) -> dict[str, Any]:
        records = await current_records(
            [r for r in fixtures if topic.casefold() in r.title.casefold()]
        )
        return {"items": [evidence_record_payload(r, synthetic=True, level=engine.grade(r).value)
                          for r in records], "mode": "fixture-only",
                "summary": engine.summarize(records), "disclaimer": DISCLAIMER}

    @app.get("/api/v1/evidence/export/citation")
    async def citation_export(topic: str = Query(default="", max_length=120)) -> dict[str, Any]:
        records = await current_records(
            [r for r in fixtures if topic.casefold() in r.title.casefold()]
        )
        payloads = [evidence_record_payload(r, synthetic=True, level=engine.grade(r).value)
                    for r in records]
        return {**build_citation_export(payloads), "source_mode": "fixture-only"}

    @app.get("/api/v1/evidence/{identifier}")
    async def evidence_record(identifier: str) -> dict[str, Any]:
        record, = await current_records([fixture_by_identifier(identifier)])
        return {"item": evidence_record_payload(
            record, synthetic=True, level=engine.grade(record).value,
        ), "mode": "fixture-only", "disclaimer": DISCLAIMER}

    def fixture_by_identifier(identifier: str) -> EvidenceRecord:
        for record in fixtures:
            if record.identifier == identifier:
                return record
        raise HTTPException(404, {"code": "NOT_FOUND", "message": "Evidence fixture not found"})

    @app.post("/api/v1/evidence/{identifier}/review")
    async def review_evidence_record(
        identifier: str,
        body: EvidenceReviewRequest,
        x_review_key: str | None = Header(default=None),
    ) -> dict[str, Any]:
        if not reviewer_key:
            raise HTTPException(503, {"code": "REVIEW_DISABLED",
                                      "message": "Server-side review key is not configured"})
        if not x_review_key or not secrets.compare_digest(x_review_key, reviewer_key):
            raise HTTPException(401, {"code": "UNAUTHORIZED",
                                      "message": "An operator review key is required"})
        record = fixture_by_identifier(identifier)
        try:
            reviewed = apply_human_review(
                record,
                status=body.status,
                reviewer=body.reviewer,
                reviewed_at=body.reviewed_at,
                notes=body.notes,
            )
        except ValueError as exc:
            raise HTTPException(422, {"code": "INVALID_REVIEW", "message": str(exc)}) from exc
        payload = evidence_record_payload(
            reviewed, synthetic=True, level=engine.grade(reviewed).value
        )
        event = await require_review_repository().record_event(
            record_identifier=reviewed.identifier,
            status=reviewed.review_status.value,
            reviewer=reviewed.reviewed_by or "",
            reviewed_at=reviewed.reviewed_at or "",
            notes=reviewed.review_notes or "",
            payload=payload,
        )
        return {"mode": "review-event", "item": event, "disclaimer": DISCLAIMER}

    @app.get("/api/v1/evidence/{identifier}/review-events")
    async def review_events(
        identifier: str,
        after_id: int = Query(default=0, ge=0),
        limit: int = Query(default=50, ge=1, le=100),
    ) -> dict[str, Any]:
        fixture_by_identifier(identifier)
        events, next_after_id = await require_review_repository().list_for_record(
            identifier, after_id=after_id, limit=limit,
        )
        return {"mode": "review-events", "items": events, "limit": limit,
                "next_after_id": next_after_id, "disclaimer": DISCLAIMER}

    @app.get("/api/v1/research-gaps")
    def gaps(topic: str = Query(min_length=1, max_length=120)) -> dict[str, Any]:
        gaps_found = ResearchGapDetector(engine).detect(topic, fixtures)
        return {"mode": "fixture-only", "disclaimer": DISCLAIMER,
                "items": [asdict(gap) for gap in gaps_found]}

    @app.get("/api/v1/graph")
    def graph() -> dict[str, Any]:
        return {"mode": "fixture-only", "nodes": ["illustrative gene", "illustrative pathway"],
                "edges": [{"source": "illustrative gene", "target": "illustrative pathway",
                           "relation": "synthetic association"}], "disclaimer": DISCLAIMER}

    @app.get("/api/v1/{resource}")
    def unavailable(resource: str) -> None:
        raise HTTPException(404, {"code": "RESOURCE_UNAVAILABLE",
                                  "message": "This resource is not implemented in this preview"})
    return app
