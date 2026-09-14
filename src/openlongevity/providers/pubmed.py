"""NCBI E-utilities PubMed adapter (read-only)."""

from datetime import UTC, datetime
from os import getenv
from xml.etree import ElementTree

import httpx

from .base import LiteratureProvider, Provenance, ProviderError, Publication, SearchQuery


class PubMedProvider(LiteratureProvider):
    name = "pubmed"
    _base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    async def search(self, query: SearchQuery) -> list[Publication]:
        params = {
            "db": "pubmed",
            "term": query.query,
            "retmode": "json",
            "retmax": query.limit,
            "retstart": (query.page - 1) * query.limit,
            "tool": "openlongevity",
            "email": getenv("NCBI_EMAIL", ""),
        }
        async with httpx.AsyncClient(timeout=20, follow_redirects=False) as client:
            try:
                response = await client.get(f"{self._base}/esearch.fcgi", params=params)
                response.raise_for_status()
                ids = response.json().get("esearchresult", {}).get("idlist", [])
                if not ids:
                    return []
                xml_response = await client.get(
                    f"{self._base}/efetch.fcgi",
                    params={"db": "pubmed", "id": ",".join(ids), "retmode": "xml"},
                )
                xml_response.raise_for_status()
                return self._parse(xml_response.text)
            except (httpx.HTTPError, ValueError, ElementTree.ParseError) as exc:
                raise ProviderError("PubMed request or XML parsing failed") from exc

    async def get_by_id(self, external_id: str) -> Publication | None:
        records = await self.search(SearchQuery(f"{external_id}[PMID]", limit=1))
        return records[0] if records else None

    def _parse(self, xml: str) -> list[Publication]:
        root = ElementTree.fromstring(xml)
        now = datetime.now(UTC).isoformat()
        records: list[Publication] = []
        for article in root.findall(".//PubmedArticle"):
            pmid = article.findtext(".//PMID")
            title = " ".join(article.findtext(".//ArticleTitle", default="").split())
            if not pmid or not title:
                continue
            abstract = " ".join(
                " ".join(node.itertext()).strip() for node in article.findall(".//AbstractText")
            )
            journal = article.findtext(".//Journal/Title")
            doi = next(
                (
                    node.text
                    for node in article.findall(".//ArticleId")
                    if node.attrib.get("IdType") == "doi"
                ),
                None,
            )
            authors = tuple(
                " ".join(filter(None, (node.findtext("LastName"), node.findtext("ForeName"))))
                for node in article.findall(".//Author")
            )
            records.append(
                Publication(
                    identifier=f"PMID:{pmid}",
                    title=title,
                    abstract=abstract,
                    authors=tuple(name for name in authors if name),
                    journal=journal,
                    doi=doi,
                    provenance=Provenance(
                        "pubmed", f"PMID:{pmid}", f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/", now
                    ),
                )
            )
        return records
