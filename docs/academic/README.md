# OpenLongevity academic document set

This collection turns the platform specification into reviewable research notes. Each document states a question, a method, a Mermaid figure, and reproducibility checks. The documents describe infrastructure and evaluation plans; none is a clinical efficacy claim.

| ID | Document | Focus |
| --- | --- | --- |
| A01 | [System architecture](01-system-architecture.md) | boundaries and data flow |
| A02 | [Evidence ontology](02-evidence-ontology.md) | typed record semantics |
| A03 | [Provider provenance](03-provider-provenance.md) | source traceability |
| A04 | [Causal inference boundary](04-causal-inference-boundary.md) | association versus causation |
| A05 | [Biomarker validation](05-biomarker-validation.md) | analytical and clinical validity |
| A06 | [Multi-omics integration](06-multi-omics-integration.md) | sample-keyed joins |
| A07 | [Survival analysis](07-survival-analysis.md) | censoring and estimands |
| A08 | [Research-gap detection](08-research-gap-detection.md) | transparent prioritization |
| A09 | [Model evaluation](09-model-evaluation.md) | calibration and subgroup error |
| A10 | [Reproducibility protocol](10-reproducibility-protocol.md) | rerunnable releases |
| A11 | [Data governance](11-data-governance-ethics.md) | privacy and responsible AI |
| A12 | [Federated evidence retrieval](12-federated-evidence-retrieval.md) | multi-registry read-only querying |
| A13 | [Confounding and covariate adjustment](13-confounding-covariate-adjustment.md) | causal-diagram-based adjustment sets |
| A14 | [Longitudinal biomarker trajectories](14-longitudinal-biomarker-trajectories.md) | mixed-effects trajectory modeling |
| A15 | [Genomic variant evidence tiering](15-genomic-variant-evidence-tiering.md) | rubric-based variant tiers |
| A16 | [Aging clock benchmarking](16-aging-clock-benchmarking.md) | external-cohort generalization |
| A17 | [Adverse event signal surfacing](17-adverse-event-signal-surfacing.md) | safety signals without auto-causal claims |
| A18 | [Meta-analysis heterogeneity](18-meta-analysis-heterogeneity.md) | pooled effects with heterogeneity reporting |
| A19 | [Access control and role model](19-access-control-role-model.md) | reader/annotator/curator separation |
| A20 | [Intervention comparability](20-intervention-comparability.md) | PICO-based trial comparability scoring |
| A21 | [Versioned release and rollback](21-versioned-release-rollback.md) | immutable, tagged evidence releases |
| A22 | [API contract and provenance envelope](22-api-contract-provenance-envelope.md) | response contracts and traceability requirements |
| A23 | [Persistence architecture](23-persistence-architecture.md) | PostgreSQL persistence and database-specific tests |
| A24 | [Monorepo governance](24-monorepo-governance.md) | atomic cross-language review vs. polyrepo cost |
| A25 | [Threat model and adversarial input](25-threat-model-adversarial-input.md) | untrusted text, prompt injection, dependency risk |
| A26 | [Data source catalog and licensing](26-data-source-catalog-licensing.md) | read-only boundary across five registries |
| A27 | [Documented limitations as epistemic boundary](27-documented-limitations-epistemic-boundary.md) | falsifiable, checkable scope statements |
| A28 | [Independent audit methodology](28-independent-audit-methodology.md) | forensic verification of maturity claims |
| A29 | [Human review boundary for machine extraction](29-human-review-boundary-machine-extraction.md) | verification as an irreducibly human action |
| A30 | [Worked example as reproducible protocol](30-worked-example-fixture-boundary.md) | tutorial discipline and the fixture/observation boundary |
| A31 | [Release notes as scientific changelog](31-release-notes-scientific-changelog.md) | capability claims paired with documented limits |

## Status and interpretation of the collection

The collection contains thirty-one numbered notes. A01–A11 and A22–A23 have been expanded during the documentation audit to develop their questions, implementation boundaries, failure cases, and evaluation protocols. The author's other extensions are preserved and remain part of the expansion backlog. Their presence in this index does not imply that every proposed method is implemented or independently validated. The corpus-wide word-count report distinguishes expanded documents from shorter research outlines.

Read a note's implementation statements against the commit it identifies. A protocol may describe a future federated query service, a role model, an external-cohort benchmark, or a human-review workflow without establishing that the repository executes that method. The purpose of the collection is to make those research designs examinable. It should not become a catalog of advertised product features merely because each topic has a formal title and a diagram.

The most immediate technical reference is [the whitepaper](../../WHITEPAPER.md), which corrects several earlier discrepancies between examples and code. The [API reference](../API.md) distinguishes persisted publication operations from fixture-based evidence demonstrations. Those two documents help a reader interpret the numbered notes without assuming that every diagram depicts a connected production pipeline.

## Reading paths for different questions

A researcher examining the meaning of evidence can begin with A02, then read A04, A05, and A08. Together they distinguish record structure, causal interpretation, measurement validation, and local coverage signals. The sequence is useful because a well-formed record can still support an inappropriate interpretation. It encourages the reader to ask what the source actually establishes before considering how software ranks or displays it.

A developer examining data movement can begin with A01 and A03, then consult A22, A23, and A25 as more specialized design notes. The critical questions are which boundaries currently exist, what provenance survives them, and how failures are classified. A type definition or database table is not sufficient evidence that the full path is operational. Trace a concrete item and preserve the distinction between a proposed contract and an observed execution.

An analyst evaluating computational routines can begin with A06, A07, A09, and A10. These notes discuss sample linkage, survival representation, model evaluation, and reproducibility artifacts. A14, A16, and A18 extend the research agenda into longitudinal trajectories, aging-clock benchmarks, and synthesis. The extended notes should be read as methodological starting points pending fuller development and corresponding implementation evidence.

An auditor examining responsibility can begin with A11, A27, A28, and A29. The relevant questions concern scope, provenance, access, correction, and accountable review. A named author provides responsibility for the project but does not establish external review or institutional endorsement. Audit claims should identify the evidence inspected and should preserve unresolved limitations rather than treat a formal document structure as proof of maturity.

## What constitutes a complete academic note

A complete note should state a concrete question and explain why the chosen representation or method addresses it. It should identify the unit of analysis and describe assumptions that would change the interpretation if they failed. It should distinguish implementation observations, methodological proposals, and empirical results. Where no empirical evaluation exists, it should provide a falsifiable evaluation protocol rather than invent a favorable result.

Examples should serve a specific purpose. A small synthetic calculation can verify an interface or arithmetic convention, while a real-source example can examine traceability. Neither should be substituted for the other. Code should use actual imports and constructor fields, and the text should explain whether an example has been executed. A diagram should identify proposed components and should not imply that a human-review service exists solely because a reviewer node has been drawn.

References should support the adjacent claim and retain the original authors' credit. Project authorship does not transfer authorship of an external method or study. Prefer the originating standard, provider documentation, or research publication when explaining a specific technical decision. A reference list is not a substitute for reasoning: the note still needs to explain the decision made for OpenLongevity and the limitations of that decision.

## Editorial checks and revision discipline

The documentation auditor counts prose after excluding fenced code, diagram source, inline code, and link targets. The minimum of one thousand words is a measurable editorial requirement, not a certification of scholarly quality. The audit also checks author attribution, local file targets, code-fence closure, and the presence of diagrams in numbered academic notes. Mermaid syntax is checked separately; rendering and visual clarity require their own review.

When revising a note, preserve the original question and useful contributions while correcting unsupported claims directly. Explain substantive behavior changes in the relevant implementation or release record. Do not inflate the word count with repeated disclaimers, duplicated method sections, or fabricated experiments. The intended result is a collection whose reasoning can be challenged and whose examples can be examined, with a transparent backlog wherever that standard has not yet been reached.

---

**Author (A12–A31 extension).** Ciprian Ștefan Pleșca — independent Romanian researcher.

**License.** Licensed under the Apache License, Version 2.0. You may not use this file except in compliance with the License. You may obtain a copy at http://www.apache.org/licenses/LICENSE-2.0. Distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
