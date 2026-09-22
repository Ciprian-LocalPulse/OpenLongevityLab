from unittest.mock import AsyncMock

import pytest
from httpx import MockTransport, Response

from openlongevity.origins import PublicationOrigin, publication_origin_fields
from openlongevity.providers.base import SearchQuery
from openlongevity.providers.pubmed import PubMedProvider


def test_search_query_is_normalized_and_bounded() -> None:
    query = SearchQuery("  cellular   senescence ", limit=5)
    assert query.query == "cellular senescence"
    with pytest.raises(ValueError):
        SearchQuery("x", limit=101)


def test_pubmed_xml_parser_preserves_provenance() -> None:
    xml = """
    <PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>123</PMID>
    <Article><ArticleTitle>Example aging study</ArticleTitle>
    <Abstract><AbstractText>Reported observation.</AbstractText></Abstract>
    <Journal><Title>Research Journal</Title></Journal></Article></MedlineCitation>
    <PubmedData><ArticleIdList>
      <ArticleId IdType="doi">10.1000/example</ArticleId>
    </ArticleIdList></PubmedData>
    </PubmedArticle></PubmedArticleSet>
    """
    records = PubMedProvider()._parse(xml)
    assert records[0].identifier == "PMID:123"
    assert records[0].doi == "10.1000/example"
    assert records[0].provenance is not None
    assert records[0].provenance.source_provider == "pubmed"
    assert records[0].origin == PublicationOrigin.UNKNOWN


@pytest.mark.parametrize(
    ("payload", "expected_origin", "expected_synthetic"),
    [
        ({}, PublicationOrigin.UNKNOWN, None),
        ({"origin": "manual"}, PublicationOrigin.MANUAL, None),
        ({"origin": "provider"}, PublicationOrigin.PROVIDER, False),
        ({"origin": "synthetic"}, PublicationOrigin.SYNTHETIC, True),
        ({"origin": "provider", "synthetic": True}, PublicationOrigin.SYNTHETIC, True),
        ({"origin": "not-a-real-origin"}, PublicationOrigin.UNKNOWN, None),
        ({"identifier": "SYN-001", "origin": "provider"}, PublicationOrigin.SYNTHETIC, True),
        ({"identifier": "SEED-0001"}, PublicationOrigin.SYNTHETIC, True),
    ],
)
def test_publication_origin_fields_are_conservative(
    payload: dict[str, object],
    expected_origin: PublicationOrigin,
    expected_synthetic: bool | None,
) -> None:
    assert publication_origin_fields(payload) == {
        "origin": expected_origin,
        "synthetic": expected_synthetic,
    }


async def test_pubmed_search_marks_standard_live_path_as_provider() -> None:
    provider = PubMedProvider()
    provider._request = AsyncMock(  # type: ignore[method-assign]
        side_effect=[
            Response(200, json={"esearchresult": {"idlist": ["123"]}}),
            Response(200, text=_pubmed_xml("123", "Provider path aging study")),
        ]
    )
    records = await provider.search(SearchQuery("aging", limit=1))
    assert records[0].origin == PublicationOrigin.PROVIDER


async def test_pubmed_search_does_not_certify_injected_transport_as_provider() -> None:
    provider = PubMedProvider(transport=MockTransport(lambda request: Response(500)))
    provider._request = AsyncMock(  # type: ignore[method-assign]
        side_effect=[
            Response(200, json={"esearchresult": {"idlist": ["456"]}}),
            Response(200, text=_pubmed_xml("456", "Injected transport aging study")),
        ]
    )
    records = await provider.search(SearchQuery("aging", limit=1))
    assert records[0].origin == PublicationOrigin.UNKNOWN


def _pubmed_xml(pmid: str, title: str) -> str:
    return f"""
    <PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>{pmid}</PMID>
    <Article><ArticleTitle>{title}</ArticleTitle>
    <Abstract><AbstractText>Reported observation.</AbstractText></Abstract>
    <Journal><Title>Research Journal</Title></Journal></Article></MedlineCitation>
    </PubmedArticle></PubmedArticleSet>
    """
