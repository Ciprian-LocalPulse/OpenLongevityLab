"""Publication identity and immutable retrieval revisions.
Revision ID: 0001_publications
Revises: none
"""
import sqlalchemy as sa
from alembic import op

revision = "0001_publications"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("publications",
        sa.Column("identifier", sa.String(160), primary_key=True),
        sa.Column("provider", sa.String(40), nullable=False),
        sa.Column("source_identifier", sa.String(100), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("first_retrieved_at", sa.String(40), nullable=False),
        sa.Column("last_retrieved_at", sa.String(40), nullable=False),
        sa.UniqueConstraint("provider", "source_identifier", name="uq_publication_source"))
    op.create_table("publication_revisions",
        sa.Column("publication_id", sa.String(160),
                  sa.ForeignKey("publications.identifier", ondelete="CASCADE"), primary_key=True),
        sa.Column("revision", sa.Integer(), primary_key=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("retrieved_at", sa.String(40), nullable=False))

def downgrade():
    op.drop_table("publication_revisions")
    op.drop_table("publications")

