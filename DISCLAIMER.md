# Disclaimer

OpenLongevity is research software. It does not provide medical advice, diagnosis, clinical treatment recommendations, or proof of human longevity benefit.

## Intended research use

The project supports inspection of research metadata, experimental computational methods, and evidence-navigation concepts. Its intended use is to help researchers and developers examine how information is represented and transformed. This document describes that boundary; it is not a regulatory classification or an approval for a particular deployment. The suitability of a system for a specialized use cannot be established merely by naming the use in documentation.

OpenLongevity currently contains components at different maturity levels. Publication persistence and selected API operations coexist with synthetic demonstrations and proposed methodological designs. A reader should identify the component and version actually used before interpreting an output. The project does not become a validated scientific platform solely because it has an extensive academic collection, an attractive interface, or a package version associated with a planned milestone.

## Bibliographic records are not verified findings

A publication record identifies scholarly material and selected metadata. Successful retrieval and parsing can demonstrate that software obtained and represented that material, but they do not establish that every conclusion in the source is correct. They also do not establish that a generated summary accurately describes the study. The source's design, population, endpoint, analysis, and limitations remain necessary to interpret its findings.

A publication can contain several observations, and several publications can describe the same study or cohort. Counting records therefore does not necessarily count independent evidence. OpenLongevity does not currently implement a comprehensive study-identity or cohort-reconciliation service. A summary based on record counts should state the unit counted and avoid implying independence that the system has not established.

Correction and retraction information also has a limited scope. A supported parser indicator is useful, but unknown status is not proof that a current comprehensive check found no notice. Reviewers may need to inspect the provider and original publication before relying on a disputed item. Local content history records changes in the representation; it is not automatically a complete history of scientific corrections.

## Scores and categories have specific meanings

The A–G mapping is a project-specific study-design convention for navigation. It does not replace assessment of risk of bias, measurement quality, or relevance to the question. The current grading implementation also maps retracted records to G, so the original design and retraction status must remain available together. A single letter cannot communicate every dimension needed for scientific interpretation.

The numerical navigation score combines heuristic factors and has not been calibrated as a probability that a claim is true. It is not an effect size, clinical benefit estimate, or recommended action. Publication-age weighting also depends on the current UTC time. A report using the score should preserve its inputs, code version, time basis, and limitations rather than turn a convenient numeric range into a stronger scientific meaning.

Research-gap and contradiction signals are similarly bounded. They examine patterns within selected records under simple rules. An empty local search does not establish absence of evidence in the world, and opposing direction labels do not establish that two studies examined comparable endpoints. These outputs can guide reading and review, but they cannot replace the methodological work needed to assess coverage or reconcile findings.

## Synthetic examples and origin labels

Synthetic fixtures are artificial inputs used to demonstrate or test behavior. They are not observations from real studies or participants. Evidence, research-gap, and graph demonstrations currently use such material. A screenshot, export, or summary should retain that origin so that a demonstration is not mistaken for a scientific result after it is separated from the application.

The current persisted publication response has a known origin-label limitation: serialization fixes the synthetic flag to false rather than deriving it from a verified origin record. Manually seeded synthetic content can therefore receive that flag. Users and operators should not treat the field alone as proof of genuine provider retrieval. This document identifies the limitation; resolving it requires an implementation correction and regression tests.

Realistic formatting does not change origin. A provider-shaped envelope, a plausible title, or a numeric identifier can be present in test data. Source authenticity requires a traceable acquisition record and appropriate verification, not only resemblance to a normal response. The project should make this distinction explicit wherever fixtures and persisted records are presented together.

## Experimental analysis and biological interpretation

The regression baseline, survival utility, pathway routine, and multi-omics helper are computational components with specific limitations. A successful call demonstrates behavior for the supplied input, not suitability for every research design. The baseline is not an externally validated aging clock. The survival utility does not provide a complete causal or competing-risk analysis. Multi-omics grouping does not establish assay harmonization or participant consistency.

The pathway adjustment has a documented implementation limitation and should not be described as validated false-discovery-rate control until corrected and tested against appropriate reference cases. More broadly, a mathematical routine needs a defined question, assumptions, input quality, and evaluation design before its output can support a scientific interpretation. The [whitepaper](WHITEPAPER.md) and relevant academic notes explain current boundaries.

A change in a biomarker, a model prediction, and a change in lifespan are different outcomes. Evidence in cells or animals does not automatically establish an effect in humans. An association does not automatically identify a causal intervention effect. OpenLongevity's research orientation should preserve those distinctions without converting a navigation result into individual treatment or supplement guidance.

## Review, deployment, and responsibility

Review-state fields do not establish an operational reviewer authorization service. A verified label needs an accountable process identifying the claim, source revision, reviewer, decision, and rationale. The repository does not claim that such a complete service has been independently evaluated. Similarly, a successful local test or health response does not establish production readiness, complete security, or a verified public deployment.

Operators are responsible for the scope and configuration of their actual instance. Sensitive participant data is outside the default public-metadata workflow and requires a separate justified assessment. The project's general privacy and security documents cannot certify an environment that has not been examined. See [privacy](PRIVACY.md), [security](SECURITY.md), and [data governance](DATA_GOVERNANCE.md) for the specific project expectations.

Project authorship belongs to Ciprian Ștefan Pleșca, an independent Romanian researcher, while original studies and third-party methods retain their own credit. No affiliation, endorsement, independent benchmark, or clinical validation should be inferred from citations or presentation style. If a document or output overstates a capability, report the specific discrepancy so it can be corrected. A general disclaimer does not remove the responsibility to repair a concrete misleading claim.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
OpenLongevity · [Project repository](https://github.com/Ciprian-LocalPulse/OpenLongevityLab).
