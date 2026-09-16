# Privacy

The default deployment analyzes public scientific information and synthetic examples. Human-subject datasets require lawful collection, consent where applicable, de-identification, access controls, retention limits, and governance review. Logs must exclude secrets and sensitive personal information.

## Scope of this repository policy

This document describes privacy expectations for OpenLongevity's source code and research workflows. It is not a deployment-specific notice for every instance someone may host. Hosting providers, logging configuration, analytics, access management, and database contents can differ between deployments. An operator must describe the actual handling of information in their instance before making promises about collection, retention, or deletion to users.

The repository's default research scope is public scholarly metadata and synthetic demonstrations. That scope does not establish permission to collect personal health histories, upload private cohort tables, or process participant identifiers through a public service. A future integration involving such material needs its own documented purpose and appropriate assessment. The project should not broaden its practical data boundary merely because a generic upload or text field could accept additional content.

## Information categories and likely exposure paths

Public publication metadata can include author names, affiliations, identifiers, titles, and abstracts where supplied by a provider. Those fields remain associated with their original research sources. Public availability does not make every possible reuse appropriate or eliminate source-specific terms. Preserve provenance and use only the information needed for the stated research operation rather than accumulating unrelated details for unspecified future analysis.

Queries can also reveal information. A person searching for a condition or intervention may enter a name, identifier, or personal context unnecessarily. The current application does not need such information to demonstrate literature navigation. Operators should explain appropriate query use and inspect whether server or proxy logs retain query strings. This policy does not assert that every hosting layer has been configured to avoid that retention.

Operational data may include request identifiers, timestamps, errors, and connection metadata. Debugging can expose response bodies or configuration values if logging is not controlled. A deployment inventory should identify which layers collect which fields, who can access them, and why they are retained. The absence of an analytics package in one source file would not establish that the entire deployed service collects no operational information.

## Data minimization in development and support

Use synthetic examples when real personal information is unnecessary. A parser test can reproduce malformed structure without including a participant record. A bug report can use a reduced payload rather than a complete database export. A screenshot can show a placeholder record while preserving the interface defect. These choices reduce exposure and often make the reproduction easier to inspect.

Before sharing logs, examine them for database URLs, ingestion keys, tokens, query content, and source text that should not be redistributed. Do not assume that redacting one visible credential removes every copy from a transcript or artifact. A support request should state what was removed and preserve only the details needed to understand the problem. Sensitive security reports should use [the private reporting path](SECURITY.md).

Repository commits are especially important to review because later deletion from the current file does not necessarily remove information from history or copied repositories. Preventing an unnecessary commit is preferable to attempting cleanup afterward. This policy does not promise that the project can erase every distributed copy of material once published. Operators and contributors should consider that persistence before including real personal information in an example.

## Participant-level research data

Any proposed participant dataset should have a defined research purpose, access basis, data dictionary, linkage policy, retention plan, and responsible operator. Describe which identifiers are necessary and where mappings are held. A pseudonymous sample label can still support linkage across datasets, so the assessment should consider combinations of fields and context rather than only direct names.

Access should reflect the tasks performed. A developer testing a parser may not need the underlying participant table. A reviewer assessing an extracted publication claim may not need individual measurements. An exported aggregate may have different disclosure risks from the input data. Document those distinctions and evaluate the specific proposed release rather than treating one access approval as permission for every downstream use.

The current project does not establish a complete participant-data governance service. Review fields, an operator key, and a database revision table are not substitutes for the necessary access, oversight, and handling processes. If prerequisites are unmet, the dataset should remain outside the default workflow. This is a boundary on the project's scope, not a retrospective assurance that unreviewed processing would be safe.

## Retention, correction, and deletion

Define retention according to purpose and environment. Temporary debugging material, source responses, normalized publication records, and scientific outputs need not be retained for the same duration. The policy for an actual deployment should identify the retained artifacts and explain how backups, caches, and derived exports are handled. Do not promise immediate universal deletion if the system lacks the controls to perform it.

Correction and deletion can have different scientific consequences. A bibliographic error may require correcting a record while preserving enough history to explain earlier outputs. An accidental secret or inappropriate personal-data inclusion may require a different response. Identify the affected copies and access paths, then document the action taken without repeating the sensitive content in a public explanation.

The current publication history supports local content revisions but is not a complete privacy-request workflow. It does not automatically determine which artifacts must be retained or deleted. An operator should define responsibility for receiving requests and verifying the applicable scope before deploying a service that collects user information. This repository does not invent a contact address or a response-time guarantee for an operator who has not supplied them.

## Transparency and user communication

A deployment-specific notice should describe actual information handling in language users can understand. Identify the operator, purposes, categories, recipients or service providers where relevant, retention approach, and available contact route. Keep that notice aligned with configuration changes. Adding analytics or account functionality changes the facts and requires review rather than reliance on this general repository policy.

OpenLongevity's author is Ciprian Ștefan Pleșca, an independent Romanian researcher. That attribution is not a statement that the author operates every deployed fork or instance. Users should know which operator is responsible for the service they are using. Source-code authorship, hosting responsibility, and research-data responsibility can belong to different parties and should not be conflated.

## Verification and related guidance

Privacy verification should inspect real data flows, logs, exports, configuration, and access controls under the intended deployment. Test that synthetic labels survive presentation and that secret values do not appear in routine failures. Review support artifacts before publication and document unresolved gaps. A policy's existence is not evidence that those checks have passed.

See [data governance](DATA_GOVERNANCE.md), [research ethics](RESEARCH_ETHICS.md), and [the academic governance note](docs/academic/11-data-governance-ethics.md) for related responsibilities. The objective is specific, inspectable handling of information within a justified scope. This document provides engineering and project-policy expectations; it does not certify an unexamined deployment or replace the assessment required for a particular research setting.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
