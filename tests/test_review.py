import pytest

from openlongevity.models import EvidenceRecord, ReviewStatus, StudyType
from openlongevity.review import apply_human_review, require_human_verified


def record() -> EvidenceRecord:
    return EvidenceRecord(
        "REAL-001",
        "Human-reviewed senescence evidence",
        StudyType.OBSERVATIONAL,
        "human",
        "senescence marker",
        "provider fixture",
        confidence=0.7,
        tags=("senescence",),
    )


def test_human_review_sets_verified_with_metadata() -> None:
    reviewed = apply_human_review(
        record(),
        status=ReviewStatus.VERIFIED,
        reviewer="Ciprian Ștefan Pleșca",
        reviewed_at="2026-09-21T10:00:00+03:00",
        notes="Checked against source fields and provenance.",
    )
    assert reviewed.review_status is ReviewStatus.VERIFIED
    assert reviewed.reviewed_by == "Ciprian Ștefan Pleșca"
    assert reviewed.reviewed_at == "2026-09-21T10:00:00+03:00"
    assert reviewed.review_notes == "Checked against source fields and provenance."
    assert reviewed.confidence == 0.7


def test_human_review_rejects_machine_status() -> None:
    with pytest.raises(ValueError, match="human review can only set"):
        apply_human_review(
            record(),
            status=ReviewStatus.MACHINE_EXTRACTED,
            reviewer="Reviewer",
            reviewed_at="2026-09-21T10:00:00+03:00",
            notes="Automated extraction is not verification.",
        )


def test_human_review_requires_metadata() -> None:
    with pytest.raises(ValueError, match="reviewer is required"):
        apply_human_review(
            record(),
            status=ReviewStatus.VERIFIED,
            reviewer=" ",
            reviewed_at="2026-09-21T10:00:00+03:00",
            notes="Checked.",
        )
    with pytest.raises(ValueError, match="review notes are required"):
        apply_human_review(
            record(),
            status=ReviewStatus.VERIFIED,
            reviewer="Reviewer",
            reviewed_at="2026-09-21T10:00:00+03:00",
            notes=" ",
        )


def test_require_human_verified_rejects_unverified_records() -> None:
    with pytest.raises(ValueError, match="not human verified"):
        require_human_verified(record())


def test_require_human_verified_requires_metadata() -> None:
    incomplete = EvidenceRecord(
        "REAL-002",
        "Incomplete verified record",
        StudyType.OBSERVATIONAL,
        "human",
        "senescence marker",
        "provider fixture",
        review_status=ReviewStatus.VERIFIED,
    )
    with pytest.raises(ValueError, match="missing human review metadata"):
        require_human_verified(incomplete)
