"""Vercel serverless entrypoint.

Vercel's Python runtime looks for a file under `api/` that exposes an ASGI
(or WSGI) callable named `app`. This module wires that up to the existing
FastAPI application defined in `openlongevity.api.create_app()`, without
duplicating any application logic.
"""
import sys
from pathlib import Path

# The `openlongevity` package lives under src/ (src layout). Vercel's default
# dependency install does not install this project itself as a package, so we
# add `src/` to the import path explicitly rather than relying on it being
# pip-installed.
_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from openlongevity.api import create_app  # noqa: E402

app = create_app()
