"""Interfaces for licensed scientific source adapters."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SourceDocument:
    identifier: str
    title: str
    abstract: str
    source: str
    license: str | None = None
    retrieved_at: str | None = None


class LiteratureAdapter(Protocol):
    source_name: str

    def search(self, query: str, *, limit: int = 20) -> list[SourceDocument]: ...


def validate_query(query: str, *, max_length: int = 200) -> str:
    normalized = " ".join(query.split())
    if not normalized:
        raise ValueError("query must not be empty")
    if len(normalized) > max_length:
        raise ValueError(f"query must not exceed {max_length} characters")
    return normalized
