-- PostgreSQL schema for provenance-preserving scientific evidence.
CREATE TABLE IF NOT EXISTS publications (
    identifier TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    source TEXT NOT NULL,
    publication_date DATE,
    retraction_status TEXT NOT NULL DEFAULT 'unknown'
        CHECK (retraction_status IN ('active','corrected','expression_of_concern','retracted','unknown')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS evidence_records (
    identifier TEXT PRIMARY KEY,
    publication_identifier TEXT REFERENCES publications(identifier),
    study_type TEXT NOT NULL,
    species TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    confidence DOUBLE PRECISION NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    replication_status TEXT NOT NULL DEFAULT 'unknown',
    limitations JSONB NOT NULL DEFAULT '[]'::jsonb,
    provenance JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS evidence_records_study_type_idx ON evidence_records(study_type);
