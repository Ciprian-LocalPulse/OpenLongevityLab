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
