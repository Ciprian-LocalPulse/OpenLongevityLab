# Research ethics

The project distinguishes correlation from causation, preclinical from clinical evidence, and computational hypotheses from observations. It avoids direct clinical recommendations, unsupported rejuvenation claims, and redistribution of restricted datasets.

## Scope and ethical responsibility

OpenLongevity is research software for organizing evidence and examining computational methods. Its default data boundary consists of public scholarly metadata and synthetic examples. This document states project expectations for responsible work within that boundary and identifies decisions that would require additional assessment before expanding it. It is not an institutional ethics approval, a clinical-use authorization, or a claim that every future deployment satisfies all applicable obligations.

The project author and maintainer is Ciprian Ștefan Pleșca, an independent Romanian researcher. That attribution identifies responsibility for project direction and communication. It does not imply oversight by a university, hospital, or government laboratory. Where independent expertise or formal review is needed, the project should state the need and record the actual review obtained rather than imply that an ethics document itself supplies approval.

## Scientific claims should remain proportionate

A research statement should identify what was observed, in which setting, and under which design. A cellular experiment, an animal study, an observational association, and a randomized comparison answer different questions. Shared biological terminology does not eliminate the distance between those settings. OpenLongevity should preserve species, endpoint, population context, and limitations instead of summarizing heterogeneous records as a single claim of benefit.

Numerical scores require the same discipline. The current navigation score uses heuristic weights; it is not a probability of truth or a measure of treatment effect. A graph relationship is not automatically causal. A model that predicts an age-related target is not automatically a measure of an individual's health or an intervention's ability to extend life. The ethical requirement is to prevent the interface and documentation from implying more than the method establishes.

Uncertainty should remain visible when results are shortened or exported. A carefully qualified paragraph can become misleading if a card title drops the population, comparator, or time horizon. Review the formats people actually use to share information, including screenshots and summaries. An export that preserves a source URL but loses the distinction between fixture and observation is still inadequate for responsible interpretation.

## Data acquisition and participant boundaries

Before acquiring a new source, identify the intended purpose, permitted use, content category, and handling requirements. Public availability is not a complete assessment of whether content can be retained, redistributed, or combined with other information. The project should record what was checked and preserve unknowns. Do not infer a favorable rights status merely because an API request succeeds.

Participant-level datasets are outside the default public-metadata workflow. A future study involving such data needs an appropriate account of authorization, consent where relevant, access, retention, and risks arising from linkage or disclosure. Removing direct names does not by itself explain whether a dataset is suitable for public release. The specific study and deployment require their own assessment before ingestion, rather than retrospective justification after data have been committed.

Synthetic examples should be used when real personal data are unnecessary for a software test. Their construction and origin should be documented. Realistic-looking values can help exercise an interface but must not be presented as observations from participants. The current origin-labeling defect in persisted publication responses is therefore a substantive ethical and engineering concern, not merely a cosmetic wording issue.

## Machine assistance and accountable interpretation

Automated extraction can assist with organization, but generated text must remain distinguishable from source content. Preserve the passage and transformation information needed to inspect a proposed finding. A machine's confidence-looking output does not establish that the extraction was correct, and fluent prose does not establish that a conclusion follows from the study. A named human remains responsible for claims published under the project's authorship.

Human review should be specific enough to be accountable. Identify what was reviewed, which source revision was consulted, who made the decision, and why. A verified status without that context can create unwarranted authority. The current repository's review fields are not a complete operational review service. Documentation must retain the distinction between representing a review state and enforcing a trustworthy process for assigning it.

Source documents may contain instruction-like text. A future language-model workflow should treat such material as data rather than permission to reveal secrets, change tools, or publish claims. Test this boundary with deliberately adversarial synthetic inputs. The ethical objective is to preserve the user's authorized task and the integrity of research records even when the retrieved material is malformed or manipulative.

## Fair evaluation and negative findings

Evaluation should be designed to discover failures, not only to produce a favorable metric. Define the target, population, comparison method, and evaluation procedure before interpreting performance. Include unsuccessful predictions, missing records, and difficult parser cases in the report. Removing them without explanation can create a misleading impression of reliability even when every reported calculation is arithmetically correct.

Negative and inconclusive findings should remain part of the research record. A failed replication, an unknown replication status, and an absence of indexed records are different observations. The project should not collapse them into one unfavorable category or ignore them when summarizing a topic. Likewise, a source correction or retraction should trigger examination of affected interpretations rather than disappear from a clean-looking interface.

Subgroup analyses need justified definitions, adequate context, and explicit uncertainty. Sensitive attributes should not be collected or disclosed merely because they might be useful for a table. A model evaluation should explain the purpose of each analysis and the limitations of available data. The project currently reports no independently established fairness or clinical-performance certification for its experimental models.

## Interests, funding, and communication

Financial support and commercial interests should be disclosed when they materially relate to a contribution or claim. A donation should not purchase a favorable evidence classification, a review outcome, or an unsupported endorsement. The project's funding communication should describe actual needs and uses without promising discoveries or health benefits that have not been established. Scientific interpretation remains constrained by evidence irrespective of sponsorship.

Public communication should make the project's independent status and maturity clear. References to demanding academic standards express an aspiration for rigor, not affiliation with a named institution. Do not invent collaborators, peer reviewers, approvals, or impact statistics. Readers should be able to evaluate the methods and provenance without being persuaded by credentials or endorsements that the project does not possess.

## Correction and continuing examination

When a problem is discovered, identify affected artifacts and the practical consequence. A mislabeled fixture may require withdrawing an example from scientific interpretation; a parser error may require reprocessing; a methodological error may invalidate an output. Preserve the reasoning behind the correction and tell readers what changed. A general research-use disclaimer does not remove responsibility for correcting a specific misleading claim.

Related guidance appears in [data governance](DATA_GOVERNANCE.md), [privacy](PRIVACY.md), [the causal-inference note](docs/academic/04-causal-inference-boundary.md), and [the academic manifesto](ACADEMIC_MANIFESTO.md). The ethical objective is a project whose decisions can be inspected and challenged, with clear responsibility and proportionate claims. It is an ongoing practice demonstrated through artifacts and corrections, not a status conferred by the length or tone of this document.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
