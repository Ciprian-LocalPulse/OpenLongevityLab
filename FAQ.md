# FAQ

OpenLongevity cannot tell anyone how long they will live and cannot recommend supplements or treatments. Animal or cellular evidence does not establish human efficacy. Biological age is a research construct with multiple operational definitions. AI-generated summaries are hypotheses or navigation aids until a human reviewer confirms their sources.

## What is OpenLongevity at the current stage?

It is a research-software prototype with partially integrated infrastructure. The repository contains typed evidence models, metadata adapters, a PostgreSQL publication path, API routes, experimental analysis utilities, and a TypeScript interface shell. These parts have different maturity levels. The presence of a module or an academic note does not mean that the corresponding end-to-end workflow is complete. The [whitepaper](WHITEPAPER.md) identifies important implementation boundaries.

## Who is responsible for the project?

Ciprian Ștefan Pleșca is the founder, principal author, and lead maintainer, described as a cercetător român independent, or independent Romanian researcher. The project does not claim affiliation with a university or government laboratory merely because it aspires to rigorous documentation. Original publications, external methods, and third-party software retain their own authorship. See [the author record](AUTHORS.md) for the distinction between project responsibility and source credit.

## Does a publication shown in the database mean its findings were verified?

No. Bibliographic retrieval, successful parsing, and local storage establish different facts from scientific verification. A publication can be genuine while an extracted interpretation is inaccurate or incomplete. Review of a particular claim needs its source passage, study context, relevant revision, and accountable decision. The current publication repository does not implement a complete scientific adjudication service, and a stored revision is not a peer-review record.

## Which API responses use real persistence and which are demonstrations?

Publication listing, title search, detail, and history use the configured PostgreSQL repository. PubMed ingestion retrieves and saves publications under an operator-key control. Evidence and research-gap routes currently operate on synthetic fixtures, and the graph response is illustrative. These paths should remain distinguishable in any interface or export. See [the API reference](docs/API.md) for request shapes, bounds, and failure behavior.

## Can the synthetic flag alone prove that a publication is genuine?

Not in the current implementation. Publication serialization fixes the flag to false rather than deriving it from a verified origin model. A synthetic record inserted directly into storage can therefore receive an inappropriate flag. This is a documented implementation limitation requiring a code-level fix and regression test. Operators should retain the origin of test data and should not treat a provider-shaped envelope as sufficient proof of authenticity.

## Is search a full-text or systematic-review search engine?

Current persisted search filters publication titles. It does not search every field or full article text, and it does not establish exhaustive coverage of a scientific topic. A systematic review requires a documented search and selection method appropriate to its question. An empty result from the local index means that the current query found no matching stored records; it does not prove that no relevant research exists elsewhere.

## What do the A–G categories mean?

The implemented mapping assigns systematic reviews to A, randomized trials to B, clinical studies to C, observational studies to D, animal studies to E, in-vitro studies to F, and computational studies to G. This is a project navigation convention, not the GRADE framework or a universal quality assessment. Retraction currently also maps a record to G, so original study type and publication status must remain visible together.

## Is the navigation score a probability or an effect estimate?

No. It combines hand-selected design weights with confidence, replication metadata, sample size, and publication age. Its value helps organize a review queue under those assumptions. It has not been calibrated as a probability that a claim is true and does not estimate an intervention effect. Dated scores also depend on the current UTC time. The whitepaper documents the actual arithmetic and its limitations.

## Does a research-gap signal prove that an area is unexplored?

It describes a rule activated within the selected records. The detector uses text matching and simple category or metadata checks, not an exhaustive survey of the field. A concentration signal may reflect a shared provider label rather than a single independent research group. A useful next step is source review and broader searching. The [gap-detection note](docs/academic/08-research-gap-detection.md) explains these counterexamples.

## Is the biological-age module ready for personal health interpretation?

The module is an ordinary-least-squares baseline for computational demonstrations. The repository does not establish an externally validated aging clock or individual medical interpretation. A model evaluation needs a defined target, population, split strategy, comparison method, and uncertainty analysis. A successful fit on synthetic data is evidence about that software example, not evidence that the model measures a person's health or predicts their lifespan.

## Do multi-omics joins perform biological harmonization?

The current helper groups feature dictionaries by sample identifier and layer. It preserves explicit missing values but does not correct batch effects, validate participant consistency, or resolve repeated sample-layer entries safely. Duplicate entries can overwrite earlier values. A cohort workflow needs additional identity, unit, preprocessing, and missingness controls. The [multi-omics note](docs/academic/06-multi-omics-integration.md) separates the implemented join from those proposed capabilities.

## Can I reproduce results without contacting an external provider?

Some parser and computational behaviors can be reproduced through offline fixtures and examples. That is useful for isolating local regressions. A live-source check answers a different question and can change as upstream records evolve. Record the exact commit, environment, inputs, and command for either type of run. [Reproducibility guidance](REPRODUCIBILITY.md) explains the difference and the additional requirements for database tests.

## Why can tests pass while the product remains a prototype?

Tests establish the behaviors they exercise under their configuration. They do not automatically establish complete coverage, browser usability, secure deployment, or scientific validity. A skipped integration case remains unverified. The current frontend scripts invoke type checking rather than a complete production build and interaction-test suite. Maturity claims should name the evidence supporting them instead of treating one successful command as approval of the whole platform.

## Why are some academic notes longer than others?

The corpus is undergoing an explicit expansion to at least one thousand prose words per tracked Markdown file. Foundational notes and selected technical references have been developed first, while other outlines remain in the backlog. Code and Mermaid source do not count toward the threshold. The audit reports incomplete files openly. Length is a minimum editorial requirement; accuracy, distinct reasoning, executable examples, and appropriate references still need review.

## Can I contribute a dataset, correction, or methodological criticism?

Yes, through a focused contribution with clear provenance and permitted-use information. Use synthetic or appropriately shareable examples for software defects, and identify the affected commit and expected behavior. A methodological criticism should identify the assumption or claim being challenged and provide supporting reasoning. Do not upload private participant data or credentials to a public issue. See [contribution guidance](CONTRIBUTING.md) and [data governance](DATA_GOVERNANCE.md).

## Where should a security issue be reported?

Use the private GitHub vulnerability-reporting channel identified in [the security policy](SECURITY.md). Include a minimal reproduction and affected revision without publishing secrets or unnecessary source data. The policy distinguishes reporting, investigation, remediation, and disclosure and does not invent a guaranteed response deadline. Ordinary documentation corrections can use normal project discussion, while sensitive exploit details should remain in the private reporting path.

## Does financial support influence scientific conclusions?

Support is optional and should fund maintenance and development rather than purchase a finding, evidence grade, or review outcome. The [support page](DONATE.md) describes the author's supplied payment channels and nonfinancial contributions. No donation establishes clinical benefit, independent validation, or an institutional partnership. Scientific claims remain constrained by source evidence, methodological review, and the project's [governance process](GOVERNANCE.md).

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
