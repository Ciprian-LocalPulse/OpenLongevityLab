# Glossary

This glossary defines terms as they are used in OpenLongevity and identifies places where a project field has a narrower meaning than the corresponding scientific concept. Definitions support interpretation; they do not establish that every described method is implemented or that a particular study has been validated.

## Research objects and scientific interpretation

**Publication.** A bibliographic object such as an article or indexed report. One publication may describe several experiments, and multiple publications may arise from one study. A publication identifier therefore does not by itself establish an independent unit of scientific evidence.

**Study.** A planned investigation with a defined design, population or experimental system, measurements, and analysis. The current publication repository does not comprehensively resolve study identity across articles. Counting stored publications is not necessarily equivalent to counting independent studies.

**Evidence observation.** A structured account of something reported under a study's conditions. In OpenLongevity, an `EvidenceRecord` carries selected characteristics such as design, species, endpoint, direction, and limitations. It remains distinct from bibliographic metadata and from a subsequent interpretation.

**Claim.** An assertion derived from or associated with observations. A claim should identify its scope and inferential level. Successful retrieval of a source does not establish that the claim accurately represents the source or follows from the study design.

**Endpoint.** The outcome or measurement specified for a research comparison. Interpretation needs its definition, scale, timing, and relevant comparator. A free-text endpoint label is useful for a prototype but may not contain enough information for statistical synthesis or causal interpretation.

**Association.** A relationship observed in data under a particular collection and analysis process. An association may help formulate a hypothesis, but it is not automatically an intervention effect. Direction, population, measurement, and possible alternative explanations remain part of its interpretation.

**Causal estimand.** A precisely defined target quantity describing a causal question under specified conditions. It should identify the relevant population, intervention contrast, outcome, and time horizon. The current graph and navigation score do not supply causal identification merely by displaying a relationship.

**Biomarker.** A measured characteristic used in a specified biological or research context. Its interpretation depends on measurement and intended use. A marker associated with an outcome is not automatically a validated surrogate for an intervention's effect. The [FDA–NIH BEST resource](https://www.ncbi.nlm.nih.gov/books/NBK326791/) supplies detailed terminology.

**Biological age.** A research construct operationalized through a particular model or measurement definition. Different targets and methods can yield different meanings. OpenLongevity's regression baseline does not establish a universal biological-age quantity or provide individual clinical interpretation.

**Healthspan.** A duration defined in relation to a specified state of health or function. Research must operationalize the state, measurement, and transition criteria. The term should not be treated as a self-evident outcome interchangeable across studies with different definitions.

**Lifespan.** The duration of life under a defined observation framework. In research, species, population, time origin, and incomplete follow-up affect what can be estimated. A change in a laboratory marker does not by itself establish a change in lifespan.

## Project evidence and review fields

**Evidence category.** The project's A–G study-design mapping, used for navigation. It is not a universal risk-of-bias assessment or the GRADE framework. The current implementation also assigns retracted records category G, making it necessary to retain original design and publication status separately.

**Navigation score.** A bounded heuristic product of design weight and selected metadata factors. It helps order review under explicit assumptions. It is not a probability of truth, effect size, or validated certainty measure, and dated inputs introduce a dependence on execution time.

**Confidence field.** A numeric value in a model or rule output whose meaning depends on that component. A number between zero and one is not automatically a calibrated probability. Consumers should inspect how the value was assigned before interpreting or comparing it.

**Replication status.** Metadata describing an assessment of corroboration under a stated convention. Unknown status is different from an assessed failure to replicate. The current free-text conventions require careful interpretation and do not independently establish the design or independence of a replication study.

**Retraction status.** A representation of publication-related notices or their absence from the current record. Unknown is not an affirmative finding that no notice exists. A supported parser indicator is useful but may not constitute a comprehensive current verification of the source.

**Review status.** A represented stage of assessment, such as unreviewed or verified. Field values alone do not enforce reviewer identity, authorization, or adequate source inspection. A trustworthy review process needs the reviewed claim, source revision, decision, rationale, and responsible person.

**Research-gap signal.** A heuristic activated by a pattern in selected indexed records. It can prioritize further reading but does not establish absence of research outside the collection. Query behavior, source coverage, and rule definitions constrain its meaning.

**Apparent contradiction.** A candidate disagreement surfaced for examination. Opposite direction labels may arise from different endpoints, populations, or coding conventions. The current tag-based routine does not establish comparability or resolve the scientific disagreement automatically.

## Provenance and persistence

**Provenance.** Information about source objects, transformations, and responsibility that helps reconstruct how a record was produced. The [W3C PROV model](https://www.w3.org/TR/prov-dm/) provides a general reference. OpenLongevity's compact envelope does not claim complete conformance to that model.

**Source identifier.** An identifier meaningful within an upstream provider's namespace. It should remain separate from a locally assigned record key. Converting one into the other without preserving the mapping can make source inspection and deduplication unreliable.

**Parser version.** An identifier for extraction logic handling a source representation. It is distinct from normalization version and package version. Recording it helps explain why the same source material may yield a different normalized record after an implementation change.

**Normalization.** A documented transformation into a common representation, such as a date or identifier convention. It can lose information and should therefore be versioned and examined. A normalized value is not necessarily a more scientifically accurate value.

**Checksum.** A digest computed from a specifically defined artifact. Its interpretation requires knowing what was hashed. Canonicalized XML, raw response bytes, and normalized JSON are different objects; their hashes cannot be treated as interchangeable evidence of identity.

**Publication revision.** A stored version of normalized publication content under repository rules. It describes local representation history, not necessarily an upstream correction or scientific review. Database revision storage is not inherently a tamper-proof ledger.

**Idempotence.** A property describing the effect of repeating an operation under specified conditions. Repeated unchanged retrieval and repeated changed-content ingestion have different expected histories. The claim must identify the operation and state being compared rather than serve as a general reliability label.

## Analysis and verification

**Synthetic fixture.** Artificial input constructed to test or demonstrate software behavior. It is not a scientific observation. Origin labeling must survive persistence and display, and plausible metadata should not allow the fixture to be mistaken for a genuine publication or participant record.

**Censoring.** In the survival utility, the representation of follow-up ending without an observed event at that time. The indicator does not validate the censoring assumptions. Event definition, time origin, and the study process remain necessary for interpreting the resulting curve.

**Data leakage.** Use of information in model development that would not appropriately be available under the intended evaluation or prediction setting. Related samples, duplicated participants, and preprocessing fitted across a held-out set are examples requiring an explicit study-aware split strategy.

**Calibration.** Agreement between a probabilistic output's stated probabilities and relevant observed frequencies under an evaluation design. The current ordinary-least-squares baseline does not emit those probabilities. A confidence-looking project field should not be assumed calibrated without evidence.

**Reproducibility.** The ability to repeat a specified computation or reconstruct a result with identified artifacts and conditions. It should be reported at the operation level. Reproducing software output does not establish that its scientific interpretation or underlying measurement is valid.

**Validation.** An evaluation against requirements appropriate to an intended use. Structural schema checks, reference calculations, external-cohort evaluation, and clinical utility studies address different questions. A report should name the kind of validation performed and avoid promoting one kind into another.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
