"""Bounded NCBI E-utilities ingestion with injectable HTTP transport."""
import asyncio
import hashlib
from datetime import UTC, datetime
from os import getenv
from xml.etree import ElementTree

import httpx
from defusedxml.ElementTree import fromstring
from defusedxml.common import DefusedXmlException

from .base import Provenance, ProviderError, Publication, SearchQuery


class PubMedProvider:
    name = "pubmed"
    _base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    max_bytes = 5_000_000

    def __init__(self, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self.transport = transport
        self._lock = asyncio.Lock()

    async def _request(
        self, client: httpx.AsyncClient, endpoint: str, params: dict[str, str | int]
    ) -> httpx.Response:
        for attempt in range(3):
            await asyncio.sleep(0.35)  # <3 requests/s in a single provider instance
            try:
                async with client.stream("GET", f"{self._base}/{endpoint}", params=params) as resp:
                    content = bytearray()
                    async for chunk in resp.aiter_bytes():
                        content.extend(chunk)
                        if len(content) > self.max_bytes:
                            raise ProviderError("PubMed response exceeded the configured limit")
                    response = httpx.Response(resp.status_code, headers=resp.headers,
                                              content=bytes(content), request=resp.request)
                if response.status_code == 429 or response.status_code >= 500:
                    if attempt < 2:
                        retry = response.headers.get("retry-after", "")
                        delay = min(float(retry), 10.0) if retry.isdigit() else 0.5 * 2**attempt
                        await asyncio.sleep(delay)
                        continue
                response.raise_for_status()
                return response
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                if attempt == 2:
                    raise ProviderError("PubMed transport failed after three attempts") from exc
                await asyncio.sleep(0.5 * 2**attempt)
            except httpx.HTTPStatusError as exc:
                raise ProviderError("PubMed returned an unsuccessful HTTP status") from exc
        raise ProviderError("PubMed request exhausted its retry budget")

    async def search(self, query: SearchQuery) -> list[Publication]:
        params: dict[str, str | int] = {
            "db": "pubmed", "term": query.query, "retmode": "json",
            "retmax": query.limit, "retstart": (query.page - 1) * query.limit,
            "tool": "openlongevity", "email": getenv("NCBI_EMAIL", ""),
        }
        # Serialize one instance's calls. Multi-worker limits require a shared gateway.
        async with self._lock, httpx.AsyncClient(
            timeout=httpx.Timeout(20, connect=5), follow_redirects=False,
            transport=self.transport, headers={"User-Agent": "OpenLongevity/0.3.0"}
        ) as client:
            response = await self._request(client, "esearch.fcgi", params)
            try:
                payload = response.json()
                ids = payload["esearchresult"]["idlist"]
                if not isinstance(ids, list) or any(
                    not isinstance(value, str) or not value.isdigit() for value in ids
                ):
                    raise ValueError("Invalid PubMed identifiers")
            except (ValueError, KeyError, TypeError) as exc:
                raise ProviderError("PubMed returned malformed search data") from exc
            if not ids:
                return []
            fetched = await self._request(client, "efetch.fcgi", {
                "db": "pubmed", "id": ",".join(ids[:query.limit]), "retmode": "xml"
            })
            return self._parse(fetched.text)

    async def get_by_id(self, external_id: str) -> Publication | None:
        pmid = external_id.removeprefix("PMID:")
        if not pmid.isdigit():
            raise ValueError("A numeric PMID is required")
        records = await self.search(SearchQuery(f"{pmid}[PMID]", limit=1))
        return next((record for record in records if record.identifier == f"PMID:{pmid}"), None)

    def _parse(self, xml: str) -> list[Publication]:
        if len(xml.encode()) > self.max_bytes:
            raise ProviderError("PubMed response exceeded the configured limit")
        try:
            root = fromstring(xml)
        except (ElementTree.ParseError, DefusedXmlException) as exc:
            raise ProviderError("PubMed XML is malformed or unsafe") from exc
        now = datetime.now(UTC).isoformat()
        records: list[Publication] = []
        for article in root.findall(".//PubmedArticle"):
            pmid = article.findtext("./MedlineCitation/PMID")
            title_node = article.find(".//ArticleTitle")
            title = " ".join("".join(title_node.itertext()).split()) if title_node is not None else ""
            if not pmid or not pmid.isdigit() or not title:
                continue
            abstract = " ".join("".join(node.itertext()).strip()
                                for node in article.findall(".//AbstractText"))
            types = tuple(node.text for node in article.findall(".//PublicationType") if node.text)
            retracted = "Retracted Publication" in types
            corrections = tuple(
                {"relation": node.attrib.get("RefType", "unknown"),
                 "pmid": node.findtext("PMID", default="")}
                for node in article.findall(".//CommentsCorrections")
            )
            # Hash canonicalized per-article XML, not the entire batch or retrieval timestamp.
            canonical = ElementTree.canonicalize(ElementTree.tostring(article, encoding="unicode"))
            checksum = hashlib.sha256(canonical.encode()).hexdigest()
            records.append(Publication(
                identifier=f"PMID:{pmid}", title=title, abstract=abstract,
                authors=tuple(
                    " ".join(filter(None, (node.findtext("ForeName"), node.findtext("LastName"),
                                           node.findtext("CollectiveName"))))
                    for node in article.findall(".//Author")
                ), journal=article.findtext(".//Journal/Title"),
                doi=next((node.text for node in article.findall(".//ArticleId")
                          if node.attrib.get("IdType") == "doi"), None),
                publication_date=article.findtext(".//JournalIssue/PubDate/Year"),
                publication_types=types, retraction_status="retracted" if retracted else "unknown",
                corrections=corrections,
                provenance=Provenance(
                    "pubmed", pmid, f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/", now,
                    checksum=checksum, normalization_version="2", parser_version="pubmed-2",
                )
            ))
        return records

