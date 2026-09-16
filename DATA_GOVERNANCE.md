# Data governance

Each dataset and evidence record should carry source, license status, version, retrieval date, transformation history, validation status, and correction or retraction state where applicable. This is a governance requirement, not a claim that every current model enforces it. Publication revision storage is implemented; a tamper-proof, append-only scientific review ledger is not.

## Purpose and default data scope

OpenLongevity's default scope is public scholarly metadata and clearly identified synthetic examples. This policy describes how data should be selected, represented, transformed, retained, and corrected within that scope. It does not authorize acquisition of private participant datasets or establish a complete compliance program for an unexamined deployment. A new data category requires a concrete review of its intended use and handling before ingestion.

Governance should follow data through actual operations. A provider response becomes a normalized object, may become a stored publication, and may later inform an extracted observation or research interpretation. Each transition can change meaning, lose information, or introduce a new responsibility. Keeping those transitions explicit makes it possible to examine a result rather than treat the database as one undifferentiated collection of trustworthy evidence.

## Source registration before acquisition

Create a source record identifying the provider, canonical endpoint or dataset location, responsible contact where published, retrieval method, expected content, and relevant terms. Record what has actually been checked and when. An available API key or successful request establishes access capability, not a general permission to redistribute all returned content. Unknown rights should remain unresolved instead of being replaced by the provider's name in a license field.

The source record should also describe operational limits: query bounds, pagination, response size, retry behavior, and whether the adapter supports correction notices. These details affect the interpretation of coverage. A source that returns a limited page cannot be treated as an exhaustive corpus without a documented collection strategy. Failed or incomplete acquisition should remain visible in the run record rather than become an apparently complete dataset.

Synthetic fixtures need source registration of a different kind. Identify their construction purpose, expected behavior, and artificial origin. They can verify software without representing any real publication or participant. Do not assign plausible real-world identifiers that could be confused with genuine studies. The origin distinction must survive storage, API responses, screenshots, and exports.

## Classification and field-level meaning

Classify data by content and permitted use rather than by storage location alone. Bibliographic metadata, restricted text, participant measurements, operational logs, and credentials have different handling requirements. A public repository should not contain private linkage keys simply because they were useful during debugging. A data dictionary should explain units, missing values, identifiers, and the meaning of status fields relevant to a research operation.

Source identity, local identity, and study identity should remain distinct. A publication may describe several observations, and several publications may describe one study or cohort. Counting database rows does not establish the number of independent pieces of evidence. Future entity reconciliation should document its matching rule and preserve the original identifiers so that a mistaken merge can be examined and reversed.

Unknown status is meaningful information. Unknown retraction status is not an affirmative finding that no notice exists. Unknown replication status is not a failed replication. An unavailable license is not permission. Interfaces and summaries should preserve these differences instead of mapping every missing field to a reassuring default. Schema changes may be necessary when the current representation cannot express an important distinction.

## Transformation records and data quality

Record the transformation applied to each retained artifact, including parser, normalization policy, configuration, and input identity. A parser version and a package version are not interchangeable. An updated parser can change normalized content while the upstream publication remains the same. A quality review should therefore examine the reason for a changed value instead of assuming that every local revision reflects a new scientific source event.

Quality checks should be tied to a purpose. Structural validation can reject a missing identifier or invalid type. Semantic checks can examine whether an endpoint has an interpretable unit or whether participant linkage is consistent. Scientific review can assess whether a claim accurately describes the source. Passing the first category does not establish the latter two. Reports should identify which layer was evaluated and which remains outside the check.

The current publication repository requires provenance and a checksum for its save path, but direct database insertion can bypass that workflow. The synthetic-origin flag is also currently fixed to false in publication serialization. These limitations mean that a provider-shaped payload or a stored row cannot alone establish genuine origin. An explicit origin model and regression tests are needed before the flag is relied on as an authenticity control.

## Retention, revisions, and correction

Retention should be justified by the purpose of each artifact. Raw responses, normalized records, debug logs, and reviewed research outputs need not have identical retention periods. Record the intended duration, access restrictions, and deletion procedure for the deployment rather than promise indefinite preservation by default. Consider backups and derived outputs when describing deletion; removing one database row may not remove every copy.

Publication revisions support local content history, but they are not inherently immutable. Database permissions still control alteration and deletion, and the revision structure does not substitute for an operational audit policy. A research export should identify the input revisions and transformations used so that a later correction can be related to the affected output. Historical preservation and continued endorsement of a finding are different decisions.

A correction record should identify the error, affected fields, source or implementation versions, and practical consequence. A parser correction may require reprocessing. A source retraction may require revisiting interpretations. A mislabeled synthetic record may require withdrawing an export from scientific use. Preserve the reasoning and avoid silently replacing an old conclusion with a new one that readers cannot trace.

## Access and release review

Before releasing a dataset or export, review its content, applicable rights, origin labels, identifiers, and transformation history. A metadata-only release and a full-text release have different scope. A software license does not automatically license third-party data included alongside the code. The release record should state what the project is actually distributing and avoid implying rights that have not been established.

```mermaid
flowchart LR
    S[Registered source] --> C[Classification and permitted-use review]
    C --> A[Bounded acquisition]
    A --> N[Versioned normalization]
    N --> Q[Purpose-specific quality checks]
    Q --> R[Retention and access decision]
    R --> E[Reviewed export or correction]
```

The project author and maintainer is Ciprian Ștefan Pleșca, an independent Romanian researcher. Operational responsibility must also be assigned for each deployment; a public policy cannot identify every operator's environment or data obligations. See [privacy](PRIVACY.md), [the data-source catalog](docs/data/DATA_SOURCES.md), and [the provenance note](docs/academic/03-provider-provenance.md). The aim is an inspectable chain of decisions, with unmet requirements visible rather than hidden by a general governance label.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
OpenLongevity · [Project repository](https://github.com/Ciprian-LocalPulse/OpenLongevityLab).
