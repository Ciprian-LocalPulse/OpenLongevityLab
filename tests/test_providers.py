import pytest

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
