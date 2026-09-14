"""Crossref DOI metadata adapter."""

from datetime import UTC, datetime

from .base import LiteratureProvider, Provenance, Publication, SearchQuery
from .http import request_json


class CrossrefProvider(LiteratureProvider):
    name = "crossref"
    _endpoint = "https://api.crossref.org/works"

    async def search(self, query: SearchQuery) -> list[Publication]:
        payload = await request_json(
            self._endpoint,
            params={
                "query": query.query,
                "rows": query.limit,
                "offset": (query.page - 1) * query.limit,
            },
        )
        return [
            self._parse(item)
            for item in payload.get("message", {}).get("items", [])
            if item.get("title")
        ]

    async def get_by_id(self, external_id: str) -> Publication | None:
        payload = await request_json(f"{self._endpoint}/{external_id}", params={})
        item = payload.get("message", {})
        return self._parse(item) if item.get("title") else None

    def _parse(self, item: dict) -> Publication:
        doi = item.get("DOI", "")
        title = (item.get("title") or [""])[0]
        authors = tuple(
            " ".join(filter(None, (a.get("given"), a.get("family"))))
            for a in item.get("author", [])
        )
        return Publication(
            identifier=f"DOI:{doi}",
            title=title,
            authors=tuple(a for a in authors if a),
            journal=(item.get("container-title") or [None])[0],
            doi=doi or None,
            publication_types=(
                item.get(
                    "type",
                ),
            ),
            provenance=Provenance(
                "crossref", f"DOI:{doi}", f"https://doi.org/{doi}", datetime.now(UTC).isoformat()
            ),
        )
