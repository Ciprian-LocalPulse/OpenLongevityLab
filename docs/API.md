# API

Install the optional API dependencies with `pip install -e ".[api]"`, then run:

```bash
uvicorn 'openlongevity.api:create_app' --factory --reload
```

`GET /api/v1/health` returns service and package version. `GET /api/v1/evidence?topic=senescence` queries the small synthetic fixture and returns each record's evidence grade plus a summary. Production adapters should add authentication, rate limiting, provenance persistence, and a database-backed repository before serving external traffic.
