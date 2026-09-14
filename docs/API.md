# API

Install `pip install -e ".[api]"`, then run `uvicorn 'openlongevity.api:create_app' --factory --reload`.

`GET /api/v1/health` and `/api/v1/version` expose service metadata. `/api/v1/evidence?topic=senescence` returns graded synthetic records and a summary. `/api/v1/research-gaps?topic=senescence`, `/api/v1/graph`, and `/api/v1/search?query=senescence` provide deterministic research exploration. Production adapters must add authentication, rate limiting, provenance persistence, and a database-backed repository.
