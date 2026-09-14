"""OpenAlex works adapter."""

from datetime import UTC, datetime
from os import getenv

from .base import LiteratureProvider, Provenance, Publication, SearchQuery
from .http import request_json


class OpenAlexProvider(LiteratureProvider):
    name = "openalex"
    _endpoint = "https://api.openalex.org/works"

    async def search(self, query: SearchQuery) -> list[Publication]:
        params = {"search": query.query, "per-page": query.limit, "page": query.page}
        mailto = getenv("OPENALEX_MAILTO")
        if mailto:
            params["mailto"] = mailto
        payload = await request_json(self._endpoint, params=params)
        return [
            self._parse(item)
            for item in payload.get("results", [])
            if item.get("id") and item.get("title")
        ]

    async def get_by_id(self, external_id: str) -> Publication | None:
        payload = await request_json(f"{self._endpoint}/{external_id}", params={})
        return self._parse(payload) if payload.get("id") else None

    def _parse(self, item: dict) -> Publication:
        identifier = item["id"].rsplit("/", 1)[-1]
        authors = tuple(
            a.get("author", {}).get("display_name", "") for a in item.get("authorships", [])
        )
        doi = item.get("doi")
        return Publication(
            identifier=f"OPENALEX:{identifier}",
            title=item["title"],
            authors=tuple(a for a in authors if a),
            doi=doi,
            citation_count=item.get("cited_by_count"),
            publication_date=item.get("publication_date"),
            provenance=Provenance(
                "openalex", f"OPENALEX:{identifier}", item["id"], datetime.now(UTC).isoformat()
            ),
        )
