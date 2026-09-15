"""Provider contracts and normalized source models."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol


class ProviderError(RuntimeError):
    """A recoverable upstream provider or parsing failure."""


@dataclass(frozen=True)
class SearchQuery:
    query: str
    limit: int = 20
    page: int = 1
    filters: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        normalized = " ".join(self.query.split())
        if not normalized:
            raise ValueError("query must not be empty")
        if len(normalized) > 200:
            raise ValueError("query must not exceed 200 characters")
        if not 1 <= self.limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        if self.page < 1:
            raise ValueError("page must be positive")
        object.__setattr__(self, "query", normalized)


@dataclass(frozen=True)
class Provenance:
    source_provider: str
    source_identifier: str
    source_url: str
    retrieved_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    source_updated_at: str | None = None
    license: str | None = None
    checksum: str | None = None
    normalization_version: str = "1"
    parser_version: str = "1"


@dataclass(frozen=True)
class Publication:
    identifier: str
    title: str
    abstract: str = ""
    authors: tuple[str, ...] = ()
    journal: str | None = None
    publication_date: str | None = None
    doi: str | None = None
    publication_types: tuple[str, ...] = ()
    mesh_terms: tuple[str, ...] = ()
    citation_count: int | None = None
    provenance: Provenance | None = None
    retraction_status: str = "unknown"
    corrections: tuple[dict[str, str], ...] = ()


@dataclass(frozen=True)
class ClinicalTrial:
    nct_id: str
    title: str
    official_title: str | None = None
    phase: tuple[str, ...] = ()
    status: str | None = None
    sponsor: str | None = None
    enrollment: int | None = None
    interventions: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    outcomes: tuple[str, ...] = ()
    locations: tuple[str, ...] = ()
    start_date: str | None = None
    completion_date: str | None = None
    provenance: Provenance | None = None


class LiteratureProvider(Protocol):
    """Contract shared by read-only literature and registry providers."""

    name: str

    async def search(self, query: SearchQuery) -> list[Publication]:
        """Search and normalize records from the provider."""

    async def get_by_id(self, external_id: str) -> Publication | None:
        """Retrieve one normalized record, if it exists."""
