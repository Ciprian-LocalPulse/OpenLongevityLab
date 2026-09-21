"""Export helpers that preserve the fixture/observation boundary."""

from collections.abc import Mapping
from dataclasses import asdict
from typing import Any

from .constants import DISCLAIMER
from .models import EvidenceRecord

CITATION_EXPORT_SCHEMA_VERSION = "citation-export-v1"


def evidence_record_payload(
    record: EvidenceRecord, *, synthetic: bool, level: str
) -> dict[str, Any]:
    """Serialize an evidence record with export-relevant boundary fields."""
    return {**asdict(record), "synthetic": synthetic, "level": level}


def is_synthetic_record(record: Mapping[str, Any]) -> bool:
    """Detect synthetic evidence records by explicit flag and conservative conventions."""
    identifier = str(record.get("identifier", ""))
    source = str(record.get("source", ""))
    metadata = record.get("metadata", {})
    metadata_synthetic = isinstance(metadata, Mapping) and bool(metadata.get("synthetic"))
    return (
        bool(record.get("synthetic"))
        or identifier.upper().startswith("SYN-")
        or source.casefold() == "synthetic fixture"
        or metadata_synthetic
    )


def build_citation_export(records: list[Mapping[str, Any]]) -> dict[str, Any]:
    """Build a citation-eligible export that excludes synthetic fixtures by default."""
    included: list[Mapping[str, Any]] = []
    excluded: list[dict[str, str]] = []
    for record in records:
        identifier = str(record.get("identifier", ""))
        title = str(record.get("title", ""))
        if is_synthetic_record(record):
            excluded.append({
                "identifier": identifier,
                "title": title,
                "reason": "synthetic_fixture",
            })
            continue
        included.append(record)
    return {
        "schema_version": CITATION_EXPORT_SCHEMA_VERSION,
        "mode": "citation-eligible",
        "items": included,
        "excluded": excluded,
        "total": len(included),
        "excluded_total": len(excluded),
        "disclaimer": DISCLAIMER,
    }
