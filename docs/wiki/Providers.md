# Providers

`LiteratureProvider` defines normalized search and lookup behavior. PubMed, Europe PMC, OpenAlex, and Crossref implement literature retrieval; ClinicalTrials.gov implements trial retrieval.

Every returned record includes `Provenance` with provider, source identifier, URL, retrieval time, and normalization version. Network failures raise `ProviderError` and are safe to report to API callers.
