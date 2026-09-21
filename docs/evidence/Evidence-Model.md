# Evidence Model

Author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.

## Purpose

The OpenLongevity evidence model defines how a source observation becomes a structured record without being overinterpreted. An `EvidenceRecord` describes a source observation with study design, species, endpoint, provenance, confidence, limitations, replication state, review status, direction, and retraction status. The model exists to support navigation, audit, and reproducibility. It is not a clinical decision model and does not convert a study into proof of human longevity benefit.

The evidence model separates source facts from platform-derived signals. A title, source identifier, study type, species, and endpoint belong to the record. A navigation score, contradiction flag, research-gap signal, or graph relationship is derived from one or more records. Derived signals should always link back to the records that produced them.

```mermaid
flowchart TD
  SOURCE[Source observation] --> RECORD[EvidenceRecord]
  RECORD --> DESIGN[Study design]
  RECORD --> SPECIES[Species]
  RECORD --> ENDPOINT[Endpoint]
  RECORD --> PROV[Provenance]
  RECORD --> REVIEW[Review status]
  RECORD --> LIMIT[Limitations]
  RECORD --> DERIVED[Derived signals]
  DERIVED --> SCORE[Navigation score]
  DERIVED --> CONTRA[Contradiction flag]
  DERIVED --> GAP[Research-gap signal]
```

## Core Fields

The required fields should identify the record, describe the source, and preserve the scientific context. Identifier, title, study type, species, endpoint, and source are minimal. Optional fields such as date, sample size, confidence, limitations, replication status, tags, metadata, direction, review notes, and provenance history add interpretive context. A sparse record can still be useful for discovery, but missing fields should remain visible.

Study design is mapped to a transparent hierarchy so users can distinguish systematic reviews, randomized trials, clinical studies, observational studies, animal evidence, in vitro evidence, and computational evidence. This hierarchy is a navigation aid. It does not mean a randomized trial is automatically relevant, unbiased, or sufficient. It also does not mean animal or cellular evidence is useless. The hierarchy helps users understand distance from human outcome evidence.

## Provenance

Every evidence record should retain provider identity, source identifier, source URL where available, retrieval timestamp, parser version, and license or terms context where recorded. Provenance is what allows a reviewer to trace a displayed record back to origin. Without provenance, the platform becomes a collection of claims rather than a research tool.

Provenance should also include correction and retraction state. A retracted record should remain auditable while being excluded or heavily downweighted from active evidence scoring according to documented rules. Deleting retracted records would make the platform look cleaner while making its history weaker.

## Review Status

Review status is separate from score and confidence. A machine-extracted record can have a high navigation score and still be unverified. A reviewer can verify that the record accurately represents the source without saying the source is true or clinically actionable. This distinction is central to OpenLongevity's scientific posture.

The model should support statuses such as extracted, pending review, verified, disputed, corrected, superseded, and rejected as the workflow matures. Current implementation may expose a smaller status vocabulary, but documentation should preserve the boundary: automated confidence is not human verification.

## Derived Signals

Evidence scoring, contradiction detection, graph relationships, and research-gap detection are derived signals. They help users decide what to inspect. They do not decide the truth of a field. A contradiction flag can show that two records point in different directions for similar tags or endpoints, but it cannot adjudicate which study is correct. A gap flag can show that animal evidence exists without indexed human clinical evidence, but it cannot prove absence of all human evidence.

Derived signals should carry method versions. If scoring weights or contradiction logic change, old outputs should remain interpretable. A release note should identify method changes because they may alter user attention without adding new source evidence.

## Limitations

The evidence model depends on the quality of the source and extraction. Provider metadata may be incomplete. Abstracts can omit important limitations. Study-type classification can be ambiguous. Sample size may be missing or not comparable across designs. Direction of effect may be mixed. Tags may oversimplify a complex intervention or pathway.

For that reason, the evidence model should keep uncertainty visible. A record with missing sample size should not look equivalent to a complete record. A record with mixed direction should not be forced into positive or negative language. A record derived from a fixture should be clearly synthetic and excluded from citation-eligible exports.

## Current Maturity

The repository contains a foundational evidence model and scoring utilities. Future maturity should add stronger review workflows, richer provenance history, export contracts, and tests that verify derived signals remain linked to source records. The acceptance standard is that a user can move from an output back to the evidence record and from the record back to the source. That path is what makes OpenLongevity an evidence-navigation platform rather than a claim generator.

## Acceptance Criteria

An evidence record is ready for canonical use when required fields are present, provenance is traceable, synthetic status is explicit, retraction status is represented, and review status is visible. A derived signal is ready only when it names its method version and links to the records used to compute it. A record should fail validation or remain draft if it lacks the minimum identity and source fields needed for audit.

The model should also support negative and uncertain evidence. A non-replicating study, a mixed result, or a disputed extraction should remain in the evidence map. Removing inconvenient evidence would make the platform less scientific. The goal is to represent the literature honestly, including disagreement.

## Release Obligations

Every release that changes evidence fields, score behavior, review states, or provenance semantics should update this document. If the code changes but the evidence model documentation does not, reviewers should treat that as documentation drift. The evidence model is the vocabulary through which the rest of the platform speaks.

## Audit Questions

An evidence-model audit should ask whether every displayed claim can be traced to a record, whether every record can be traced to a source, and whether every derived signal can be traced to a method version. It should also ask whether uncertainty survived the trip from source to interface. If limitations, retraction status, synthetic flags, or review status disappear from exports, the evidence model has been weakened even if the database still stores the fields.

The model should be boring in the best sense: predictable, explicit, and hard to misuse. Scientific creativity belongs in research questions and analysis; the evidence record should remain stable enough that users can argue about evidence rather than about hidden data transformations.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
