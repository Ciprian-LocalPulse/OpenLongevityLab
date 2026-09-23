"""Export helpers that preserve the fixture/observation boundary."""

import hashlib
import json
from collections import Counter
from collections.abc import Mapping
from dataclasses import asdict
from typing import Any

from .constants import DISCLAIMER
from .models import EvidenceRecord, ReviewStatus

CITATION_EXPORT_SCHEMA_VERSION = "citation-export-v1"
EVIDENCE_SCORE_METHOD_VERSION = "navigation-score-v1"


def _stable_fingerprint(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()



def evidence_record_payload(
    record: EvidenceRecord,
    *,
    synthetic: bool,
    level: str,
    navigation_score: float | None = None,
    score_method: str | None = None,
    scoring_as_of: str | None = None,
    score_components: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Serialize an evidence record with export-relevant boundary fields."""
    payload = {**asdict(record), "synthetic": synthetic, "level": level}
    if navigation_score is not None:
        payload["navigation_score"] = navigation_score
        payload["score_method"] = score_method or EVIDENCE_SCORE_METHOD_VERSION
        payload["scoring_as_of"] = scoring_as_of
        if score_components is not None:
            payload["score_components"] = dict(score_components)
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


def build_citation_export(
    records: list[Mapping[str, Any]], *, source_mode: str = "unspecified"
) -> dict[str, Any]:
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

    exclusion_reasons = Counter(item["reason"] for item in excluded)
    score_methods = sorted(
        {str(record["score_method"]) for record in records if record.get("score_method")}
    )
    scoring_times = sorted(
        {str(record["scoring_as_of"]) for record in records if record.get("scoring_as_of")}
    )
    manifest = {
        "schema_version": CITATION_EXPORT_SCHEMA_VERSION,
        "source_mode": source_mode,
        "input_records": len(records),
        "included_records": len(included),
        "excluded_records": len(excluded),
        "included_identifiers": [str(record.get("identifier", "")) for record in included],
        "excluded_identifiers": [item["identifier"] for item in excluded],
        "exclusion_reasons": dict(sorted(exclusion_reasons.items())),
        "score_methods": score_methods,
        "scoring_as_of": scoring_times,
    }
    manifest["export_fingerprint"] = _stable_fingerprint(manifest)
    return {
        "schema_version": CITATION_EXPORT_SCHEMA_VERSION,
        "mode": "citation-eligible",
        "manifest": manifest,
        "items": included,
        "excluded": excluded,
        "total": len(included),
        "excluded_total": len(excluded),
        "disclaimer": DISCLAIMER,
    }
