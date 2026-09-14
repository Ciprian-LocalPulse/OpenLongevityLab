# OpenLongevity API v1

## Run locally

```bash
pip install -e ".[dev,api]"
uvicorn 'openlongevity.api:create_app' --factory --reload
```

The service is intentionally small and explicit. Development responses use synthetic fixtures; production deployments should connect the repository and add authentication, rate limits, observability, and migrations.

## Read-only exploration

```bash
curl http://localhost:8000/api/v1/health
curl 'http://localhost:8000/api/v1/evidence?topic=senescence'
curl 'http://localhost:8000/api/v1/search?query=senescence&limit=10'
curl 'http://localhost:8000/api/v1/research-gaps?topic=senescence'
curl http://localhost:8000/api/v1/graph
```

`GET /api/v1/evidence/{record_id}` returns the normalized record, A–G grade, and navigation score. A missing record returns a structured `NOT_FOUND` error.

## Provider ingestion

```bash
curl -X POST 'http://localhost:8000/api/v1/ingestion/pubmed?query=cellular%20senescence&limit=5'
curl -X POST 'http://localhost:8000/api/v1/ingestion/clinical-trials?query=senescence&limit=5'
```

Provider failures are returned as `PROVIDER_UNAVAILABLE`; callers should retry with backoff and retain the original query. Adapters never write to external providers.

## Response and provenance contract

Every source-derived item must expose a stable local identifier plus:

```json
{
  "source_provider": "europe_pmc",
  "source_identifier": "MED:12345",
  "source_url": "https://europepmc.org/article/MED/12345",
  "retrieved_at": "2026-09-14T14:00:00+00:00",
  "normalization_version": "0.2.0"
}
```

Clients must display the disclaimer and review status with machine-extracted material. See [`WHITEPAPER.md`](../WHITEPAPER.md) for the data model and [`docs/wiki/Providers.md`](wiki/Providers.md) for adapter behavior.
