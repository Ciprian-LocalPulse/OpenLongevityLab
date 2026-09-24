# Documentation map

- `API.md` — local HTTP routes and deployment boundary.
- `evidence/Evidence-Model.md` — record semantics and grading.
- `biomarkers/Biomarkers.md` — measurement categories and limitations.
- `research/Research-Gap-Detector.md` — prioritization heuristics.
- `research/openlongevity-impact-article.md` — long-form impact article describing purpose, current stage, final target, collaboration, and donation support.
- `security/THREAT_MODEL.md` — threats and mitigations.
- `architecture/adr/` — decisions that affect long-term design.
- `academic/` — thirty-one academic research notes, with expansion status and reading paths in the collection index.

## Purpose and documentation boundary

This directory connects the implementation of OpenLongevity with the explanations needed to inspect it. The project includes a Python research core, provider adapters, publication persistence, an API, experimental analysis utilities, and an early web interface. Those components have different maturity levels. Documentation should help readers identify what is implemented, what has been tested, and what remains a proposed research method. It should not present every topic in the directory as an available product feature.

The root [README](../README.md) introduces current capabilities and installation assumptions. The [whitepaper](../WHITEPAPER.md) provides the main technical and scientific specification, including corrections to earlier examples and maturity claims. The [academic manifesto](../ACADEMIC_MANIFESTO.md) explains the project's standards for evidence and accountability. The [impact article](research/openlongevity-impact-article.md) gives an external-facing academic overview of the repository, its current research-prototype stage, its intended final form, and how collaborators or donors can support the work. This index helps readers move from those general documents to focused references without relying on the removed wiki directory.

## Start from the question you need to answer

If you need to run or integrate the HTTP application, begin with [the API reference](API.md). It distinguishes persisted publication resources from synthetic evidence and graph demonstrations. Check the exact request body, query parameters, and failure behavior before writing a client. A source file containing a route is evidence of an interface implementation; a verified deployment requires additional execution evidence from the environment where the client will run.

If you need to understand a scientific representation, begin with [the evidence model](evidence/Evidence-Model.md) and the expanded [ontology note](academic/02-evidence-ontology.md). Study design, publication status, review status, and provenance are different dimensions. A grade or score cannot stand in for all of them. The documentation should make it possible to trace a displayed statement back to the fields and assumptions used to construct it.

If you need to evaluate an analysis, read the relevant academic note before running a utility. [Multi-omics integration](academic/06-multi-omics-integration.md), [survival analysis](academic/07-survival-analysis.md), and [model evaluation](academic/09-model-evaluation.md) describe present behavior and proposed acceptance tests. Their examples demonstrate limited computational contracts. They do not establish clinical validation or show that synthetic data represent a real population.

## Navigating the academic collection

The [academic index](academic/README.md) preserves thirty-one numbered topics. A01–A11 cover foundational architecture, evidence semantics, provenance, causal interpretation, biomarkers, analysis, reproducibility, and governance. A12–A31 extend the research agenda into federation, longitudinal methods, evaluation, access, auditing, and release practices. The author's extensions remain part of the collection, with their original topics preserved during the broader documentation expansion.

The collection distinguishes a methodological proposal from implementation evidence. A proposed federation design does not establish a working federated search endpoint. A role diagram does not establish authorization enforcement. A review protocol does not establish that independent reviewers have adjudicated findings. Readers should look for the baseline commit, executable example, acceptance criteria, and reported result supporting each concrete capability claim.

Diagrams should be read with the same discipline as prose. An arrow may describe intended data flow or an implemented transfer; its caption and surrounding text should make the distinction clear. Mermaid syntax validation confirms that a parser accepts the diagram, not that the depicted architecture is correct. Visual review should also consider whether labels remain readable and whether a reader can distinguish current paths from future connections.

## Architecture, data, and operational references

Architectural decision records under `architecture/adr` explain choices intended to affect long-term design. A useful decision record states the context, alternatives, consequences, and evidence needed to revisit the choice. Short historical records in this repository remain part of the expansion backlog. Their existence does not prove that all consequences have been implemented or that a decision has been independently reviewed.

The [data-source catalog](data/DATA_SOURCES.md) and [provider-provenance note](academic/03-provider-provenance.md) address retrieval and normalization. Provider identity, source identity, retrieval time, parser version, and licensing status serve different purposes. Public access does not automatically establish redistribution rights. Unknown fields should remain unknown rather than be populated with reassuring but unverified labels.

The [threat model](security/THREAT_MODEL.md) and [root security policy](../SECURITY.md) address risks and reporting. They should be interpreted as documents whose controls require implementation evidence. An operator ingestion key is a limited access control, not a complete multiuser security model. A deployment review should examine the actual environment, configuration, data scope, and failure recovery instead of assuming security from repository prose.

## Historical records and current audit evidence

Release notes and baseline audits are historical artifacts. They should identify the version and evidence they describe. When an earlier claim proves too broad, a correction should explain the actual boundary without moving an immutable tag or implying that later code existed in the earlier release. The [v0.2.0 notes](releases/v0.2.0.md) and [v0.3.0 baseline audit](audits/v0.3.0-baseline.md) therefore need to be read with their historical scope in mind.

Current verification should report observed outcomes separately from intended checks. A test suite may pass while a database-dependent case is skipped. Type checking may pass without building a frontend. A health endpoint may respond while a provider has not been probed. These are useful but limited observations. A reliable audit retains the distinctions and identifies what evidence is still missing before a stronger maturity claim can be made.

## Editorial acceptance and contribution

The current editorial target is at least one thousand prose words for each tracked Markdown document, with consistent project-author attribution. Fenced code, Mermaid source, and link destinations are excluded from the prose count. This avoids satisfying a writing requirement by adding diagram syntax or repeated command output. The threshold is a minimum for developed explanation, not proof that a document is scientifically sound.

The documentation audit script reports short documents, missing attribution, broken local file targets, unclosed fences, and missing diagrams in numbered academic notes. It does not evaluate source accuracy, reference-link definitions, URL fragments, or visual layout. Those checks require additional review. Generated JSON reports are measurement artifacts rather than narrative documentation and should not be padded to a prose threshold.

Contributors should preserve existing useful work, correct inaccurate examples, and connect each added section to the document's purpose. A strong revision develops assumptions, a method, counterexamples, and a concrete verification plan. It should not invent benchmarks, credentials, users, partnerships, or independent review outcomes. Project attribution belongs alongside original source credits, and the exact code revision should accompany any claim that an example has been executed successfully.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
