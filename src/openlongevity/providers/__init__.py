"""Read-only scientific source adapters with explicit provenance."""

from .base import ClinicalTrial, LiteratureProvider, Publication, SearchQuery
from .clinicaltrials import ClinicalTrialsProvider
from .crossref import CrossrefProvider
from .europe_pmc import EuropePMCProvider
from .openalex import OpenAlexProvider
from .pubmed import PubMedProvider

__all__ = [
    "ClinicalTrial",
    "ClinicalTrialsProvider",
    "CrossrefProvider",
    "EuropePMCProvider",
    "LiteratureProvider",
    "OpenAlexProvider",
    "PubMedProvider",
    "Publication",
    "SearchQuery",
]
