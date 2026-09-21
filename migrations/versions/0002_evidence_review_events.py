"""Evidence review event audit table.
Revision ID: 0002_review_events
Revises: 0001_publications
"""

import sqlalchemy as sa
from alembic import op

revision = "0002_review_events"
down_revision = "0001_publications"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "evidence_review_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("record_identifier", sa.String(160), nullable=False),
        sa.Column("status", sa.String(40), nullable=False),
        sa.Column("reviewer", sa.String(120), nullable=False),
        sa.Column("reviewed_at", sa.String(40), nullable=False),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_index(
        "ix_evidence_review_events_record_identifier",
        "evidence_review_events",
        ["record_identifier"],
    )


def downgrade():
    op.drop_index(
        "ix_evidence_review_events_record_identifier",
        table_name="evidence_review_events",
    )
    op.drop_table("evidence_review_events")
