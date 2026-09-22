"""Explicit data-origin labels; provider metadata alone does not prove retrieval."""

from collections.abc import Mapping
from enum import StrEnum
from typing import Any


class PublicationOrigin(StrEnum):
    UNKNOWN = "unknown"
    MANUAL = "manual"
    PROVIDER = "provider"
    SYNTHETIC = "synthetic"


def publication_origin_fields(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize legacy records conservatively without rewriting stored history."""
    try:
        origin = PublicationOrigin(payload.get("origin", "unknown"))
    except (ValueError, TypeError):
        origin = PublicationOrigin.UNKNOWN
    identifier = str(payload.get("identifier", "")).upper()
    if payload.get("synthetic") is True or identifier.startswith(("SYN-", "SEED-")):
        origin = PublicationOrigin.SYNTHETIC
    synthetic = True if origin == PublicationOrigin.SYNTHETIC else (
        False if origin == PublicationOrigin.PROVIDER else None
    )
    return {"origin": origin, "synthetic": synthetic}
