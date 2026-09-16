# Security

Report vulnerabilities privately to the maintainers rather than in a public issue. Include a minimal reproduction and affected version without credentials or personal data.

The threat model covers API abuse, malicious datasets, dependency and action compromise, prompt injection in scientific content, path traversal, and leakage of secrets. Inputs use typed validation; source content is data, never trusted instructions. Deployments should use environment variables, least-privilege credentials, TLS, dependency review, and immutable audit logs.

Security fixes are developed against the current development line. No multi-version security maintenance guarantee or response-time service agreement is established. Include the exact commit or release in a report. See [the threat model](docs/security/THREAT_MODEL.md).

## Private vulnerability reporting

GitHub private vulnerability reporting is enabled for this repository, as checked during the documentation audit on 16 September 2026. Use the [private advisory reporting form](https://github.com/Ciprian-LocalPulse/OpenLongevityLab/security/advisories/new) for a suspected vulnerability rather than publishing exploit details in a public issue. If the form is unavailable, request a private reporting channel without including the sensitive details in the public request.

A useful report identifies the affected revision, component, prerequisites, observed behavior, and expected security boundary. Include a minimal reproduction that avoids real credentials and personal data. Explain whether the finding is based on source inspection or execution and describe the environment used. Do not attach a complete database or source response when a reduced synthetic example can demonstrate the problem.

The project is maintained by Ciprian Ștefan Pleșca, an independent Romanian researcher. This policy does not promise round-the-clock monitoring, a bug bounty, a fixed response deadline, or institutional incident-response capacity. It defines a reporting path and the evidence needed for responsible examination. Acknowledgment, investigation, remediation, and public disclosure are separate stages whose actual status should be communicated accurately.

## Threat boundary and current controls

The default application handles public research metadata and synthetic demonstrations. External source responses remain untrusted input. The PubMed path includes bounded requests, response-size checks, selected retries, and hardened XML parsing. Typed models constrain parts of the API. These controls address specific failure modes; they do not constitute a complete security assessment of the repository or every possible deployment.

PubMed ingestion requires a server-side operator key. This is a limited control over one operation, not a full identity or role-management system. The key must not be placed in a public frontend variable or embedded in a distributed browser bundle. Cross-origin settings are also not authentication: a nonbrowser client is not governed by browser cross-origin enforcement. Deployment review must consider the actual access model rather than rely on those mechanisms as interchangeable controls.

Persisted publication responses and synthetic evidence demonstrations should remain distinguishable. The current publication serialization assigns a false synthetic flag without deriving it from a verified origin model. That limitation can mislead users about manually seeded content and is documented as an integrity issue. A provenance-shaped payload is not sufficient proof of genuine source origin. Correcting the behavior requires an implementation change and regression tests.

## Secrets and environment configuration

Keep database passwords, ingestion keys, provider credentials, and deployment tokens outside version control. Configuration examples should identify variable names and use placeholders. Logs, screenshots, issue reports, and shell transcripts can expose secrets even when source files do not. Review the actual material being shared rather than assume that a private environment variable cannot reach an output.

If a credential is exposed, treat deleting the visible text as insufficient. The operator should assess where the value was accessible, revoke or rotate it through the appropriate service, and inspect relevant activity where available. The repository cannot perform those actions merely by changing a documentation file. A public incident record should describe the affected credential type and remediation scope without repeating the value.

Use credentials limited to the operations required by the deployment. A publication service should not inherit unrelated administrative privileges merely because that simplifies setup. Database access, source retrieval, release publishing, and deployment management can require different permissions. Record the intended boundary and test unauthorized operations in the actual environment. This policy describes expectations rather than claiming that every deployment already enforces them.

## Input, dependency, and workflow risks

Validate external data before using it in storage, display, or analysis. A source title may contain unusual markup or instruction-like text even when the provider host is reputable. Treat retrieved scientific content as data, never as authorization to change tools or reveal secrets. Future language-model integrations need adversarial tests for this boundary and must preserve the distinction between source material and user instructions.

Dependencies and automation workflows are part of the trust boundary. Review changes to package sources, install scripts, workflow permissions, and third-party actions according to their actual effects. A dependency scanner can identify some known issues but cannot prove that a package or workflow is safe. Record which checks ran and what they examined rather than turn a green badge into a general security guarantee.

Maintenance scripts also require scrutiny. The test seed writes directly to a configured database and may fall back from a test variable to the general database variable. Verify the destination before running it. Documentation verification tools are read-only with respect to the corpus, but their dependencies still execute locally. Install such tooling in a deliberate environment and avoid mixing it with production credentials or unrelated private data.

## Triage, remediation, and disclosure

Triage should establish the affected boundary, plausible impact, prerequisites, and reproducibility of a report. Distinguish confidentiality, integrity, availability, and misleading scientific presentation where relevant. A denial-of-service condition and an incorrect origin label have different mechanisms and mitigations. Avoid dismissing a report solely because the project is a prototype; prototype status explains maturity but does not remove the need to address concrete defects.

A remediation should include a focused change and a regression case that would detect the original issue. For data-affecting problems, identify whether existing records or exports need review or reprocessing. For configuration problems, document the environment changes required in addition to code. Passing a new test is useful evidence for the tested case, but does not establish that every related attack path has been examined.

Coordinate publication of actionable details with the people responsible for remediation. A public advisory should identify affected versions or commits, the nature of the issue, mitigation or fix, and remaining limitations. Do not invent a vulnerability identifier, severity assessment, or external audit result. If the impact remains uncertain, describe the uncertainty rather than choose a dramatic or reassuring label without evidence.

## Deployment review and ongoing limits

Before exposing an instance publicly, examine network access, credential handling, request bounds, dependency state, logging, database privileges, and recovery procedures in that instance. A local health response establishes only limited application behavior. It does not prove provider reachability, complete migration compatibility, secure configuration, or correct scientific interpretation. Required deployment evidence should be recorded separately from source-level checks.

Related guidance appears in [privacy](PRIVACY.md), [data governance](DATA_GOVERNANCE.md), and [the threat model](docs/security/THREAT_MODEL.md). This policy provides an operational reporting and review framework under the project's actual independent-maintainer structure. It does not claim a security certification, a penetration test that has not occurred, or suitability for sensitive clinical information without a separate justified assessment.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
