"""Europe PMC REST adapter."""

from datetime import UTC, datetime

from .base import LiteratureProvider, Provenance, Publication, SearchQuery
from .http import request_json


class EuropePMCProvider(LiteratureProvider):
    name = "europe_pmc"
    _endpoint = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

    async def search(self, query: SearchQuery) -> list[Publication]:
        payload = await request_json(
            self._endpoint,
            params={
                "query": query.query,
                "format": "json",
                "pageSize": query.limit,
                "page": query.page,
            },
        )
        return [
            self._parse(item)
            for item in payload.get("resultList", {}).get("result", [])
            if item.get("id") and item.get("title")
        ]

    async def get_by_id(self, external_id: str) -> Publication | None:
        payload = await request_json(
            self._endpoint,
            params={"query": f"EXT_ID:{external_id}", "format": "json", "pageSize": 1},
        )
        items = payload.get("resultList", {}).get("result", [])
        return self._parse(items[0]) if items else None

    def _parse(self, item: dict) -> Publication:
        identifier = str(item["id"])
        return Publication(
            identifier=f"EPMC:{identifier}",
            title=item["title"],
            abstract=item.get("abstractText", ""),
            journal=item.get("journalTitle"),
            publication_date=item.get("firstPublicationDate"),
            doi=item.get("doi"),
            provenance=Provenance(
                "europe_pmc",
                f"EPMC:{identifier}",
                f"https://europepmc.org/article/{item.get('source', 'MED')}/{identifier}",
                datetime.now(UTC).isoformat(),
            ),
        )
