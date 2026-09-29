from dataclasses import asdict, replace

from openlongevity.exports import (
    build_citation_export,
    build_publication_export_manifest,
    evidence_record_payload,
)
from openlongevity.models import EvidenceRecord, ReviewStatus, StudyType


def record(identifier: str = "REAL-001") -> EvidenceRecord:
    return EvidenceRecord(
        identifier,
        "Human senescence evidence",
        StudyType.OBSERVATIONAL,
        "human",
        "senescence marker",
        "provider fixture",
        confidence=0.7,
    )


def test_citation_export_includes_only_human_verified_records() -> None:
    verified = replace(
        record(),
        review_status=ReviewStatus.VERIFIED,
        reviewed_by="Reviewer",
        reviewed_at="2026-09-21T10:00:00+03:00",
        review_notes="Checked against source.",
    )
    payload = build_citation_export([asdict(verified)])
    assert payload["total"] == 1
    assert payload["excluded_total"] == 0
    assert payload["items"][0]["identifier"] == "REAL-001"


def test_citation_export_excludes_unverified_real_records() -> None:
    payload = build_citation_export([asdict(record())])
    assert payload["items"] == []
    assert payload["excluded_total"] == 1
    assert payload["excluded"][0]["reason"] == "not_human_verified"


def test_citation_export_excludes_synthetic_before_review_check() -> None:
    synthetic = evidence_record_payload(record("SYN-TEST"), synthetic=True, level="F")
    payload = build_citation_export([synthetic])
    assert payload["items"] == []
    assert payload["excluded_total"] == 1
    assert payload["excluded"][0]["reason"] == "synthetic_fixture"


def test_citation_export_manifest_summarizes_boundary_and_scoring() -> None:
    synthetic = evidence_record_payload(
        record("SYN-TEST"),
        synthetic=True,
        level="F",
        navigation_score=0.12,
        score_method="navigation-score-v1",
        scoring_as_of="2021-01-01T00:00:00+00:00",
    )

    payload = build_citation_export([synthetic], source_mode="fixture-only")

    assert payload["manifest"] == {
        "schema_version": "citation-export-v1",
        "source_mode": "fixture-only",
        "input_records": 1,
        "included_records": 0,
        "excluded_records": 1,
        "included_identifiers": [],
        "excluded_identifiers": ["SYN-TEST"],
        "exclusion_reasons": {"synthetic_fixture": 1},
        "score_methods": ["navigation-score-v1"],
        "scoring_as_of": ["2021-01-01T00:00:00+00:00"],
        "export_fingerprint": payload["manifest"]["export_fingerprint"],
    }
    assert len(payload["manifest"]["export_fingerprint"]) == 64


def test_citation_export_fingerprint_changes_with_export_boundary() -> None:
    unverified = evidence_record_payload(
        record("REAL-UNVERIFIED"),
        synthetic=False,
        level="D",
        navigation_score=0.4,
        score_method="navigation-score-v1",
        scoring_as_of="2021-01-01T00:00:00+00:00",
    )
    synthetic = evidence_record_payload(
        record("SYN-TEST"),
        synthetic=True,
        level="F",
        navigation_score=0.12,
        score_method="navigation-score-v1",
        scoring_as_of="2021-01-01T00:00:00+00:00",
    )

    first = build_citation_export([synthetic], source_mode="fixture-only")
    second = build_citation_export([synthetic, unverified], source_mode="fixture-only")

    assert first["manifest"]["export_fingerprint"] != second["manifest"]["export_fingerprint"]
    assert second["manifest"]["exclusion_reasons"] == {
        "not_human_verified": 1,
        "synthetic_fixture": 1,
    }


def test_publication_manifest_fingerprints_all_exported_metadata() -> None:
    import hashlib
    import json

    publication = {
        "identifier": "PMID:123", "title": "Metadata test", "provider": "pubmed",
        "source_identifier": "123", "origin": "unknown", "synthetic": None,
        "revision": 1, "content_hash": "a" * 64,
        "first_retrieved_at": "2026-09-22T00:00:00+00:00",
        "last_retrieved_at": "2026-09-22T00:00:00+00:00",
    }
    options = {"query": "Metadata", "page": 1, "page_size": 20, "total_matching": 1}
    result = build_publication_export_manifest([publication], **options)
    assert result == build_publication_export_manifest([publication], **options)
    assert result["mode"] == "publication-metadata-export"
    assert result["items"][0]["synthetic"] is None
    manifest = dict(result["manifest"])
    fingerprint = manifest.pop("export_fingerprint")
    encoded = json.dumps(
        {"manifest": manifest, "items": result["items"]}, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(encoded).hexdigest() == fingerprint
    assert manifest["revision_map"] == {"PMID:123": 1}
    assert manifest["content_hashes"] == {"PMID:123": "a" * 64}
    # Freshness or origin can change independently of a stored content hash.
    for field, value in (
        ("revision", 2), ("content_hash", "b" * 64), ("title", "Changed title"),
        ("last_retrieved_at", "2026-09-23T00:00:00+00:00"),
        ("origin", "manual"), ("synthetic", True),
    ):
        changed = build_publication_export_manifest([{**publication, field: value}], **options)
        assert changed["manifest"]["export_fingerprint"] != fingerprint
    changed_query = build_publication_export_manifest(
        [publication], **{**options, "query": "test"},
    )
    assert changed_query["manifest"]["export_fingerprint"] != fingerprint


def test_publication_manifest_empty_page_preserves_matching_total() -> None:
    result = build_publication_export_manifest(
        [], query="study", page=3, page_size=20, total_matching=25,
    )
    assert result["total"] == 0
    assert result["items"] == []
    assert result["manifest"]["total_matching"] == 25
    assert result["manifest"]["revision_map"] == {}
    assert result["manifest"]["exported_identifiers"] == []
