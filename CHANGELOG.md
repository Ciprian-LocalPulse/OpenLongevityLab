# Changelog

## Unreleased — documentation and integrity audit

Persisted publication responses now expose an explicit `origin` contract with `unknown`, `manual`, `provider`, and `synthetic` states plus a tri-state `synthetic` interpretation. Synthetic seeds and `SYN-*` or `SEED-*` identifiers remain synthetic even when their payload has provider-shaped metadata. Legacy rows without a documented origin are normalized conservatively as `unknown` rather than being presented as real provider retrievals. Revision history carries the normalized origin fields in each payload.

PubMed parsing remains conservative: direct XML parsing and injected transports do not certify provider origin, while the ordinary built-in PubMed search path marks records as provider-derived before persistence. Tests now cover origin normalization, PubMed path classification, provider-shaped synthetic payloads, revision changes from unknown to manual origin, API list/detail/history responses, and the CI seed record's synthetic label.

The TypeScript dashboard now presents the origin and synthetic boundaries added to the API instead of flattening persisted publications and fixture evidence into the same visual treatment. Evidence cards label synthetic fixture status, review status, level, confidence, and citation boundary; publication cards label `origin`, tri-state `synthetic`, revision, provider identifier, parser version, retrieval time, and retraction status. The knowledge-graph view now matches the implemented `/api/v1/graph` response shape, and API text is rendered through DOM nodes instead of interpolated into raw HTML.

The frontend package now uses Vite for a real production build and a Playwright-powered smoke script for rendered browser checks. The smoke test serves the built artifact, mocks API responses, exercises evidence, graph, sources, unavailable-API, desktop, and mobile states, and exits cleanly for CI. The frontend workflow installs the required Chromium browser before running these checks.

Evidence list, detail, and citation export now reconstruct current review metadata from the latest persisted event by ID. Historical events remain intact, synthetic origin remains authoritative, and configured storage failures return an error instead of stale fixture review metadata. Integration coverage exercises successive review states, deliberately backdated timestamps, and recovery through a fresh application instance.

Review-event history now uses bounded cursor pagination with a default page size of fifty and a maximum of one hundred. Clients follow `next_after_id` to retrieve subsequent pages. PostgreSQL integration coverage verifies persisted review payloads, event-ID ordering, record isolation, and continued exclusion of reviewed fixtures from citation export.

The documentation work begun from commit `9fddcbb` expands the academic corpus, corrects implementation claims, and standardizes attribution to CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent. It preserves the author's removal of the wiki and the additional academic topics. This section describes development work, not a published v0.3.0 release. Mandatory release gates remain a separate decision under the project request and governance policy.

The whitepaper now uses current evidence and multi-omics constructors, the implemented A–G mapping, and the actual navigation-score factors. It distinguishes persisted publications from synthetic evidence and graph demonstrations. The API reference now describes JSON-body PubMed ingestion, its operator key, current bounds, and title filtering. These corrections repair the explanation of existing behavior; they do not themselves repair the runtime limitations documented alongside it.

The academic expansion develops questions, assumptions, implementation boundaries, counterexamples, and acceptance protocols. Foundational notes and the API and persistence notes have been expanded first. The remaining corpus is tracked through the documentation audit instead of being described as complete. Root policies are being developed with the same standard, including contribution, governance, reproducibility, data handling, research ethics, security, and privacy.

Documentation tooling now counts prose separately from fenced code and diagrams, checks consistent author attribution, verifies local inline-link targets, and identifies selected structural problems. A separate Mermaid checker parses the diagrams under a recorded tool version. These checks have declared limits: they do not certify scientific accuracy, rendered layout, external links, or independent review. Generated results should be interpreted within that scope.

The abbreviated license file has been replaced with the official Apache License 2.0 text. Project attribution is recorded separately in NOTICE, and citation metadata identifies the author as an independent Romanian researcher. The existing release tag is preserved. The citation's release version is not silently advanced to an unpublished development version merely because the Python package declares that version.

Analysis-integrity work now includes reproducible time handling for navigation scores, plus the two targeted corrections recorded after the documentation baseline. Pathway enrichment now applies monotonic Benjamini–Hochberg adjustment over the full valid pathway family, including valid pathways with no observed overlap in the correction denominator. Multi-omics grouping now rejects duplicate sample-layer pairs and inconsistent participant mappings instead of silently overwriting earlier values. The frontend now exposes key provenance boundaries and has build-plus-browser smoke coverage, but it still needs broader accessibility, visual regression, and production deployment evidence. Publication origin classification is improved, but provider origin remains a retrieval-boundary label rather than scientific validation. No clinical validation, independent benchmark, or operational scientific review service is asserted by this documentation entry.

## [0.2.0] - 2026-09-14

- Added read-only PubMed, Europe PMC, OpenAlex, Crossref, and ClinicalTrials.gov adapters.
- Added provenance contracts, PostgreSQL persistence primitives, and initial search/API resources. Historical feature names should be read as prototype scope, not proof of complete integration or full-text retrieval.
- Added evidence navigation scoring, contradiction surfacing, translational and replication gap signals.
- Added biological-age baseline, Kaplan–Meier, pathway enrichment, and multi-omics integration modules.
- Expanded biomarker catalog and dashboard navigation; added release, governance, data-source, and limitation documentation.

## [0.1.0]

- Initial evidence model, graph abstraction, API shell, Rust kernel, and repository documentation.

## Reading historical entries

The version entries above preserve the repository's historical feature inventory. They identify areas introduced during development but should not be read as a claim that every capability was executed successfully or scientifically validated at that time. A release-specific assessment requires checking the immutable revision and its actual artifacts. Later implementation or documentation changes do not retroactively exist in an earlier tag.

This distinction is especially important for broad labels such as evidence engine, graph, persistence, or dashboard. An evidence engine may contain a heuristic rather than an empirically calibrated method. A graph may be an in-memory abstraction or fixture. A persistence primitive may precede an integrated ingestion path. A dashboard shell may type-check without producing a production build. The relevant release record should describe the concrete behavior rather than rely on the label alone.

When a historical description is too broad, add a qualification and identify the present boundary. Do not erase the fact that the earlier wording existed or move the tag to make it appear accurate. A correction can improve the current record while preserving an honest account of what readers of the earlier version encountered. This approach supports scientific traceability and ordinary software maintenance alike.

## Change categories and their consequences

A presentation change affects wording, navigation, layout, or visual interpretation. It can still matter scientifically if it changes whether a fixture or uncertainty is visible. A contract change affects fields, routes, parameters, or response semantics. A computational change affects the transformation of inputs into outputs. A data correction affects stored or distributed content. These categories help users determine whether they need to update a client, rerun an analysis, or revisit an interpretation.

For computational changes, report the affected method and the conditions under which results differ. A corrected multiple-testing adjustment, for example, needs more than a general improved statistics statement. It needs a reference case and an explanation of downstream consequences. For provenance changes, identify whether old records require migration or retain an earlier interpretation. A version number alone cannot communicate those details.

For operational changes, distinguish configuration from observed deployment. Adding a workflow or hosting file establishes an intended procedure; an actual run establishes an outcome under a particular environment. Record failed and skipped gates as well as passing ones. A successful local command should not be promoted into evidence that an externally hosted system is available or that a complete research workflow has been verified.

## Evidence expected in a release entry

A substantive release entry should identify the commit or tag, the user-visible behavior, relevant compatibility decisions, verification performed, and unresolved limitations. If a database migration is involved, state its effect and supported path. If an analysis result can change, explain why. If a source adapter changes, identify the supported source pattern and whether replay or live retrieval was examined.

Testing evidence should be concrete and proportionate. Report the command and observed outcome, including skips or environment limits. Type checking, parser fixtures, PostgreSQL integration, browser tests, and scientific evaluation answer different questions. Do not combine them into an unqualified all tests prove readiness statement. The reader needs to know which claim each check supports.

Documentation expansion is also measurable but limited. A word-count threshold indicates that a file has reached an editorial minimum, not that the argument is sound. A Mermaid parser accepting a diagram indicates syntax validity, not architecture correctness. Release notes should preserve these distinctions when describing documentation improvements so that a more professional presentation does not become an unsupported maturity claim.

## Corrections, attribution, and future entries

Project authorship remains distinct from the authorship of studies, dependencies, and external methods. Credit source material where it is used and describe contributor work accurately. A release note should not invent an external reviewer, institutional partner, benchmark result, or user-impact statistic. The project is maintained by Ciprian Ștefan Pleșca as an independent Romanian researcher, and any broader participation must be recorded from actual contributions.

Future entries should be concise about routine edits and detailed where interpretation or compatibility changes. The longer guidance here explains the discipline used to read and write those entries; it is not a requirement to repeat the same paragraphs in every release. See [the roadmap](ROADMAP.md) for planned work, [the audit](docs/audits/v0.3.0-baseline.md) for inspected evidence, and [governance](GOVERNANCE.md) for integration and release decisions.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
OpenLongevity · [Project repository](https://github.com/Ciprian-LocalPulse/OpenLongevityLab).
