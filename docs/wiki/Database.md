# Database

`openlongevity.db.Database` creates an async SQLAlchemy engine when `DATABASE_URL` is configured. `EvidenceRepository` upserts normalized evidence records and preserves serialized provenance. Schema creation is explicit so deployments can replace it with Alembic migrations.
