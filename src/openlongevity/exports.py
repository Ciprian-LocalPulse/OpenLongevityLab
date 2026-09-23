"""Export helpers that preserve the fixture/observation boundary."""

from collections.abc import Mapping
from dataclasses import asdict
from typing import Any

from .constants import DISCLAIMER
from .models import EvidenceRecord, ReviewStatus

CITATION_EXPORT_SCHEMA_VERSION = "citation-export-v1"
EVIDENCE_SCORE_METHOD_VERSION = "navigation-score-v1"


def evidence_record_payload(
    record: EvidenceRecord,
    *,
    synthetic: bool,
    level: str,
    navigation_score: float | None = None,
    score_method: str | None = None,
    scoring_as_of: str | None = None,
) -> dict[str, Any]:
    """Serialize an evidence record with export-relevant boundary fields."""
    payload = {**asdict(record), "synthetic": synthetic, "level": level}
    if navigation_score is not None:
        payload["navigation_score"] = navigation_score
        payload["score_method"] = score_method or EVIDENCE_SCORE_METHOD_VERSION
        payload["scoring_as_of"] = scoring_as_of
    return payload


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


def is_human_verified_record(record: Mapping[str, Any]) -> bool:
    """Return whether a serialized record carries human verification metadata."""
    return (
        record.get("review_status") == ReviewStatus.VERIFIED
        and bool(record.get("reviewed_by"))
        and bool(record.get("reviewed_at"))
        and bool(record.get("review_notes"))
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
        if not is_human_verified_record(record):
            excluded.append({
                "identifier": identifier,
                "title": title,
                "reason": "not_human_verified",
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
