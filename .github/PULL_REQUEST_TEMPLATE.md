# OpenLongevity Pull Request Review Template

Project author: **CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent**.

## Summary

Describe the behavior and scientific scope of this change. State what changed, why it changed, and which part of the platform is affected: evidence model, provider ingestion, persistence, API, dashboard, documentation, security, infrastructure, tests, or release process.

If the change is documentation-only, state whether it updates current implementation facts, target protocols, release history, or limitations. If the change modifies behavior, describe the before and after behavior in plain language.

## Scientific Scope

Explain what this pull request does and does not claim. OpenLongevity is a research-navigation and reproducibility platform. A pull request must not introduce unsupported medical advice, diagnosis, treatment recommendations, or proof of human longevity benefit. If the change touches biomarkers, aging clocks, interventions, survival analysis, safety signals, or clinical-trial records, include the interpretation boundary.

Examples of acceptable scoped language:

- This change adds provenance fields to exported evidence records.
- This change documents a proposed review workflow that is not yet implemented.
- This change improves fixture-based examples and keeps synthetic records labeled.
- This change updates a heuristic navigation score, not a causal effect estimate.

Examples of language that needs revision:

- This proves an intervention extends lifespan.
- This model diagnoses biological age.
- This registry entry demonstrates efficacy.
- This score establishes clinical evidence.

## Evidence and Provenance

If the pull request changes evidence records, ingestion, scoring, graph relationships, gap detection, or exports, describe how provenance is preserved. Identify source identifiers, retrieval timestamps, parser versions, review states, synthetic flags, and limitation fields that are affected. Derived outputs should remain linked to source records.

If the change uses fixtures, state that they are synthetic and whether they are excluded from citation-eligible paths. If the change uses live provider data, identify the provider and retrieval boundary. Do not include restricted datasets, private biomedical records, secrets, or full-text articles unless an explicit documented policy permits them.

## Implementation Notes

Describe the technical approach at the level a reviewer needs. Mention affected modules, schema changes, migrations, configuration variables, service boundaries, or API contracts. If a method version changes, say so. If a migration is required, identify the migration and rollback considerations. If a dependency changes, explain why it is needed.

Avoid burying scientific behavior inside implementation detail. A change to scoring, review status, provenance, or export eligibility is a scientific behavior change and should be described as such.

## Validation

List the checks performed. Include tests, lint, type checks, documentation audit, Mermaid validation, code-example execution, migration checks, or manual review. If a relevant check was not run, explain why. A skipped database test, missing deployment verification, or fixture-only check should be stated honestly.

Suggested validation commands:

```bash
ruff check .
pytest
python scripts/audit_documentation.py --json
node scripts/check_mermaid.mjs .
```

Adjust commands to the environment and current tooling. Do not claim a check passed unless it was actually run.

## Risk and Limitations

Describe residual risk. A good pull request names what remains uncertain: provider drift, partial source coverage, unreviewed extraction, fixture-only examples, missing external validation, database migration risk, UI interpretation risk, or deployment uncertainty. This section should be concise but candid.

For documentation changes, identify whether the text describes implemented behavior, release history, or future target protocol. For code changes, identify whether users can see a changed output and how the change is bounded.

## Release Notes

State whether release notes, changelog, limitations, citation metadata, or audit reports need updates. If this pull request should not affect release notes, say why. If it changes public interpretation, it probably needs release documentation.

## Checklist

- [ ] Tests and lint pass, or skipped checks are explained.
- [ ] Documentation and provenance are updated.
- [ ] No secrets, credentials, private data, or restricted datasets are committed.
- [ ] No unsupported medical, diagnostic, causal, or longevity-benefit claims are introduced.
- [ ] Synthetic fixtures remain clearly labeled and are not presented as observations.
- [ ] Licenses, source terms, and attribution are respected.
- [ ] Evidence scores remain described as transparent navigation heuristics.
- [ ] Human review status is not inferred from machine confidence.
- [ ] Breaking changes, migrations, or method-version changes are documented.
- [ ] Mermaid diagrams, if changed, parse successfully.
- [ ] Author attribution remains present where required.

## Reviewer Focus

Reviewers should prioritize scientific integrity, provenance, reproducibility, security, and user interpretation. Ask whether a reader could overstate the change. Ask whether a derived output remains traceable to source evidence. Ask whether a fixture could be mistaken for observation. Ask whether a claim in documentation matches code behavior. Ask whether a public interface preserves the limitation users need at the point of interpretation.

The goal of review is not only to prevent broken code. It is to keep OpenLongevity honest as it grows.

## Academic Quality Bar

A pull request that expands documentation should meet the same standard as code: accurate, traceable, testable where possible, and clear about scope. Long text is not automatically academic. Academic quality means the document distinguishes observation from interpretation, implemented behavior from planned protocol, and evidence navigation from clinical conclusion. If a paragraph makes a strong claim, it should either point to implementation evidence, source provenance, or a clearly labeled future requirement.

Documentation should preserve the author's identity and the independent nature of the project without implying institutional affiliation. References to external standards, providers, or research sources should not imply endorsement. Diagrams should explain actual structure or intended protocols, not decorate weak claims.

## Merge Readiness

Before merge, reviewers should be able to answer five questions. What changed? What evidence supports the claim? What checks ran? What risks remain? What user interpretation could be affected? If those questions cannot be answered from the pull request, the change is not yet ready even if the diff is syntactically correct.

When the pull request is part of release preparation, include the release version, tag target, audit status, and any known unfinished gates. Do not publish a release note that suggests a gate passed when it was skipped, unavailable, or only partially checked.

## Final Reviewer Note

Review should leave the project easier to trust. If a change is ambitious, make the ambition legible. If a feature is early, say it is early. If a result is synthetic, say it is synthetic. If evidence is unreviewed, preserve that status. The best OpenLongevity pull requests should make future researchers feel that the project is careful with uncertainty as well as capable with code.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**

OpenLongevity · [Project repository](https://github.com/Ciprian-LocalPulse/OpenLongevityLab).
