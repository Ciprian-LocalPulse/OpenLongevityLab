# Developer guide

Install `pip install -e ".[dev,api,db]"`, run `pytest` and `ruff check .`, then use `npm ci && npm run lint && npm test && npm run build` in `apps/web`. Provider adapters must remain read-only, typed, provenance-preserving, and covered by parser tests with recorded fixtures.
