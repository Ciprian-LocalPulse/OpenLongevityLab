from dataclasses import asdict, replace

from openlongevity.exports import build_citation_export, evidence_record_payload
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
