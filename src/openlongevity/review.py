"""Human review transition helpers for evidence records."""

from dataclasses import replace

from .models import EvidenceRecord, ReviewStatus

HUMAN_REVIEW_STATUSES = frozenset({
    ReviewStatus.HUMAN_REVIEWED,
    ReviewStatus.VERIFIED,
    ReviewStatus.DISPUTED,
})


def apply_human_review(
    record: EvidenceRecord,
    *,
    status: ReviewStatus,
    reviewer: str,
    reviewed_at: str,
    notes: str,
) -> EvidenceRecord:
    """Return a reviewed record while enforcing the human-review boundary."""
    if status not in HUMAN_REVIEW_STATUSES:
        raise ValueError("human review can only set human review statuses")
    reviewer = reviewer.strip()
    reviewed_at = reviewed_at.strip()
    notes = notes.strip()
    if not reviewer:
        raise ValueError("reviewer is required for human review")
    if not reviewed_at:
        raise ValueError("reviewed_at is required for human review")
    if not notes:
        raise ValueError("review notes are required for human review")
    return replace(
        record,
        review_status=status,
        reviewed_by=reviewer,
        reviewed_at=reviewed_at,
        review_notes=notes,
    )


def require_human_verified(record: EvidenceRecord) -> None:
    """Reject records that are not explicitly verified by a human reviewer."""
    if record.review_status is not ReviewStatus.VERIFIED:
        raise ValueError("record is not human verified")
    if not record.reviewed_by or not record.reviewed_at or not record.review_notes:
        raise ValueError("verified record is missing human review metadata")
